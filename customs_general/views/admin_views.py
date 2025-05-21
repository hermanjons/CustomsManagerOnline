import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from core.constants import MODEL_ICONS

from django.db.models import Q
from django.core.paginator import Paginator
from django.db import models
import io
from django.core.files.base import ContentFile
import math

from django.core.cache import cache
from django.apps import apps





@staff_member_required
def upload_excel(request, model):
    try:
        model_class = apps.get_model("customs_general", model)

        if request.method == "POST":

            if "excel_file" not in request.FILES:
                return JsonResponse({"success": False, "error": "Excel dosyası eksik!"})

            excel_file = request.FILES["excel_file"]

            try:
                if excel_file.name.endswith(".csv"):
                    df = pd.read_csv(excel_file)
                elif excel_file.name.endswith(".xlsx"):
                    df = pd.read_excel(excel_file, engine="openpyxl")
                else:
                    return JsonResponse({"success": False, "error": "Sadece .csv ve .xlsx dosyaları kabul edilir."})

                df = df.where(pd.notnull(df), None)

                field_names = []
                foreign_keys = {}
                self_relation_fields = []
                required_fields = []

                for field in model_class._meta.fields:
                    field_names.append(field.name)

                    if isinstance(field, models.ForeignKey):
                        foreign_keys[field.name] = field.remote_field.model

                        if field.remote_field.model == model_class:
                            self_relation_fields.append(field.name)

                    if not field.null and not field.blank and not isinstance(field, models.AutoField):
                        required_fields.append(field.name)

                many_to_many_fields = [field.name for field in model_class._meta.many_to_many]



                created_count = 0
                failed_rows = []
                total = len(df)


                temp_id_map = {}

                # === 1. AŞAMA: SELF-FK OLMAYAN ALANLARLA OBJELERİ OLUŞTUR ===
                for index, row in df.iterrows():
                    try:
                        record_id = row.get("id")
                        try:
                            record_id = int(record_id)
                        except (ValueError, TypeError):
                            raise TypeError("Excel'deki 'id' alanı geçerli bir sayı olmalı!")

                        obj_data = {}
                        for field in field_names:

                            val = row.get(field)
                            if val in [None, '', ' '] or (isinstance(val, float) and math.isnan(val)):

                                if field in required_fields:
                                    raise ValueError(f"Zorunlu alan eksik:{field}")
                                else:
                                    val = None
                                    obj_data[field] = val

                            else:
                                if field not in self_relation_fields and field in foreign_keys:
                                    fk_model = foreign_keys[field]
                                    val = fk_model.objects.get(id=int(val))
                                    obj_data[field] = val
                                else:
                                    obj_data[field] = val


                        obj = model_class.objects.create(**obj_data)
                        temp_id_map[record_id] = obj

                        # ManyToMany alan işlemleri
                        for m2m_field in many_to_many_fields:
                            if m2m_field in df.columns:
                                value = row.get(m2m_field)
                                if value not in [None, '', ' '] and not (
                                        isinstance(value, float) and math.isnan(value)):
                                    ids = []
                                    for val in str(value).split(','):
                                        try:
                                            ids.append(int(float(val.strip())))
                                        except ValueError:
                                            pass
                                    model_field = model_class._meta.get_field(m2m_field)
                                    related_model = model_field.related_model
                                    m2m_objs = related_model.objects.filter(id__in=ids)
                                    getattr(obj, m2m_field).set(m2m_objs)

                        created_count += 1

                    except Exception as e:
                        failed_rows.append({
                            'satir': index + 2,
                            'hata': str(e)
                        })

                    # user_views.py içinde
                    cache.set(f"upload_progress:{request.user.id}", int(((index + 1) / total*2) * 100), timeout=20)

                # === 2. AŞAMA: SELF-FK ALANLARI GÜNCELLE ===
                for index, row in df.iterrows():
                    try:
                        record_id = int(row.get("id"))
                        obj = temp_id_map.get(record_id)
                        if not obj:
                            continue

                        for field in self_relation_fields:
                            relation_id = row.get(field)
                            if relation_id is not None:
                                try:
                                    relation_id = int(relation_id)
                                    related_instance = temp_id_map.get(relation_id)
                                    if related_instance:
                                        setattr(obj, field, related_instance)
                                except Exception as e:
                                    print(f"[SelfRelation WARN] Satır {index+2}, alan '{field}': {e}")

                        obj.save()
                        user_id = getattr(request.user, "id", None)
                        progress = cache.get(f"upload_progress:{user_id}", 0)
                        cache.set(f"upload_progress:{request.user.id}", progress + int(((index + 1) / total * 2) * 100),
                                  timeout=20)

                    except Exception as e:
                        print(f"[SelfRelation ERROR] Satır {index+2}: {e}")
                        continue

                cache.set(f"failed_rows:{request.user.id}", failed_rows, timeout=300)

                return JsonResponse({
                    "success": True,
                    "message": f"{created_count} kayıt başarıyla eklendi!",
                    "failed_rows_count": len(failed_rows),
                    "failed_rows_download_url": f"/customs_general/download-failed-rows/{model}/"
                })

            except Exception as e:
                return JsonResponse({"success": False, "error": str(e)})

        else:
            return JsonResponse({"success": False, "error": "Sadece POST istekleri kabul edilir!"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})




@staff_member_required
def upload_progress(request):
    user_id = getattr(request.user, "id", None)
    if not user_id:
        return JsonResponse({"progress": 0, "debug": "user not logged in"})
    progress = cache.get(f"upload_progress:{user_id}", 0)

    return JsonResponse({"progress": progress})





@staff_member_required
def download_failed_rows(request, model):
    cache_key = f"failed_rows:{request.user.id}"
    failed_rows = cache.get(cache_key)

    if not failed_rows:
        return HttpResponse("İndirilecek hata bulunamadı.", content_type="text/plain")

    df = pd.DataFrame(failed_rows)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename={model}_hatalar.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    cache.delete(cache_key)  # İndirildikten sonra temizle (isteğe bağlı)

    return response
