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


def model_data(request, model):
    try:
        model_class = apps.get_model("customs_general", model)
    except LookupError:
        return render(request, "model_not_found.html", {"model": model})

    model_display_name = model_class._meta.verbose_name
    model_icon = MODEL_ICONS.get(model, "❓")

    query = request.GET.get("q", "").strip()
    objects = model_class.objects.all()

    if query:
        search_filters = Q()
        for field in model_class._meta.fields:
            if field.get_internal_type() in ["CharField", "TextField"]:
                search_filters |= Q(**{f"{field.name}__icontains": query})

        objects = objects.filter(search_filters)

    per_page = request.GET.get("per_page", 10)
    try:
        per_page = int(per_page) if int(per_page) in [10, 25, 50, 100] else 10
    except ValueError:
        per_page = 10

    paginator = Paginator(objects, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Modelin field bilgilerini al
    normal_fields = list(model_class._meta.fields)
    m2m_fields = list(model_class._meta.many_to_many)
    all_fields = normal_fields + m2m_fields

    field_names = [field.verbose_name for field in all_fields]
    field_keys = [field.name for field in all_fields]
    print("M2M Fields:", m2m_fields)
    return render(request, "customs_general/model_data.html", {
        "model": model,
        "model_display_name": model_display_name,
        "model_icon": model_icon,
        "page_obj": page_obj,
        "field_names": field_names,
        "field_keys": field_keys,
        "query": query,
        "per_page": per_page,
        "m2m_fields": m2m_fields,  # ⭐️⭐️⭐️ Yeni ekledik
    })


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
