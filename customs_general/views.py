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
    excluded_fields = ["created_at","updated_at","id","is_active"]

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

                # Tum dataframe icinde NaN olanlari None yapalim
                df = df.where(pd.notnull(df), None)

                field_names = [field.name for field in model_class._meta.fields if field.name != "id"]
                foreign_keys = {
                    field.name: field.remote_field.model
                    for field in model_class._meta.fields
                    if isinstance(field, models.ForeignKey)
                }
                many_to_many_fields = [field.name for field in model_class._meta.many_to_many]

                required_fields = [
                    field.name for field in model_class._meta.fields
                    if not field.null and not field.blank and not isinstance(field, models.AutoField)
                ]
                print("zorunlu alanlar:", required_fields)

                created_count = 0
                failed_rows = []
                total = len(df)
                request.session['upload_progress'] = 0

                for index, row in df.iterrows():
                    try:
                        missing_required = False

                        for field_name in required_fields:
                            val = row.get(field_name)
                            if val in [None, '', ' '] or (isinstance(val, float) and math.isnan(val)):
                                missing_required = True
                                print(f"Zorunlu alan eksik: {field_name}")
                                break

                        if missing_required:
                            raise ValueError("Eksik zorunlu alan")

                        obj_data = {}
                        for field in field_names:
                            if field not in many_to_many_fields:
                                value = row.get(field)

                                # NaN veya bos deger kontrolu
                                if value in [None, '', ' '] or (isinstance(value, float) and math.isnan(value)):
                                    value = None

                                # ForeignKey alanlar icin lookup
                                if field in foreign_keys and value is not None:
                                    fk_model = foreign_keys[field]
                                    value = fk_model.objects.get(id=int(value))

                                obj_data[field] = value

                        obj = model_class.objects.create(**obj_data)

                        # ManyToMany alanlari ayarlayalim
                        for m2m_field in many_to_many_fields:
                            if m2m_field in df.columns:
                                value = row.get(m2m_field)

                                if value not in [None, '', ' '] and not (
                                        isinstance(value, float) and math.isnan(value)):
                                    ids = []
                                    for val in str(value).split(','):
                                        val = val.strip()
                                        if val:
                                            try:
                                                ids.append(int(float(val)))
                                            except ValueError:
                                                pass
                                    model_field = model_class._meta.get_field(m2m_field)
                                    related_model = model_field.related_model
                                    m2m_objs = related_model.objects.filter(id__in=ids)
                                    getattr(obj, m2m_field).set(m2m_objs)
                                else:
                                    pass

                        created_count += 1

                    except Exception as e:
                        failed_rows.append({
                            'satir': index + 2,
                            'hata': str(e)
                        })

                    progress = int(((index + 1) / total) * 100)
                    request.session['upload_progress'] = progress

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
