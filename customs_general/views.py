from django.apps import apps
import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from core.constants import MODEL_ICONS
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from django.db import models
import io
from django.core.files.base import ContentFile
import math
from core.utils import GenericFilteredListView


class GeneralCustomsModelListView(GenericFilteredListView):
    """
    customs_general uygulamasındaki tanım modellerini listelemek için
    dinamik olarak çalışan generic view sınıfı.
    """
    app_label = "customs_general"
    model_param = "model"
    template_name = "customs_general/customs_general_page.html"
    excluded_fields = ["created_at", "updated_at", "is_active", "is_global"]

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get(self.model_param) or request.GET.get(self.model_param)
        try:
            self.model = apps.get_model(self.app_label, model_name)
        except LookupError:
            return render(request, "model_not_found.html", {"model": model_name})
        return super().dispatch(request, *args, **kwargs)


def fetch_model_detail(request, model_name, pk):
    try:
        model_class = apps.get_model("customs_general", model_name)
        obj = model_class.objects.get(pk=pk)
        data = {}

        for field in model_class._meta.fields:
            value = getattr(obj, field.name, None)
            if value is not None:
                data[field.verbose_name] = str(value)
            else:
                data[field.verbose_name] = "-"

        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


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

                field_names = [field.name for field in model_class._meta.fields]
                foreign_keys = {
                    field.name: field.remote_field.model
                    for field in model_class._meta.fields
                    if isinstance(field, models.ForeignKey)
                }
                many_to_many_fields = [field.name for field in model_class._meta.many_to_many]

                self_relation_fields = [
                    field.name for field in model_class._meta.fields
                    if isinstance(field, models.ForeignKey) and field.remote_field.model == model_class
                ]

                required_fields = [
                    field.name for field in model_class._meta.fields
                    if not field.null and not field.blank and not isinstance(field, models.AutoField)
                ]

                created_count = 0
                failed_rows = []
                total = len(df)
                request.session['upload_progress'] = 0

                temp_id_map = {}

                # === 1. AŞAMA: SELF-FK OLMAYAN ALANLARLA OBJELERİ OLUŞTUR ===
                for index, row in df.iterrows():
                    try:
                        record_id = row.get("id")
                        if record_id is None:
                            raise ValueError("Excel'de 'id' alanı boş!")
                        record_id = int(record_id)

                        # Zorunlu alan kontrolü
                        for field_name in required_fields:
                            val = row.get(field_name)
                            if val in [None, '', ' '] or (isinstance(val, float) and math.isnan(val)):
                                raise ValueError(f"Zorunlu alan eksik: {field_name}")

                        obj_data = {}
                        for field in field_names:
                            if field not in many_to_many_fields and field not in self_relation_fields:
                                value = row.get(field)
                                if value in [None, '', ' '] or (isinstance(value, float) and math.isnan(value)):
                                    value = None

                                if field in foreign_keys and value is not None:
                                    fk_model = foreign_keys[field]
                                    value = fk_model.objects.get(id=int(value))

                                obj_data[field] = value

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

                    request.session['upload_progress'] = int(((index + 1) / total) * 100)

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
                    except Exception as e:
                        print(f"[SelfRelation ERROR] Satır {index+2}: {e}")
                        continue

                request.session['upload_progress'] = 100
                request.session['failed_rows'] = failed_rows

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





def upload_progress(request):
    progress = request.session.get('upload_progress', 0)
    return JsonResponse({'progress': progress})


@staff_member_required
def download_failed_rows(request, model):
    failed_rows = request.session.get('failed_rows')

    if not failed_rows:
        return HttpResponse("İndirilecek hata bulunamadı.", content_type="text/plain")

    df = pd.DataFrame(failed_rows)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=failed_rows.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response
