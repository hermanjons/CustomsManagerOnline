from django.shortcuts import render, redirect
from django.apps import apps
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.contrib import messages, admin
from django.contrib.admin.views.decorators import staff_member_required
from .constants import MODEL_ICONS
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator


def model_data(request, model):
    try:
        model_class = apps.get_model("customs_general", model)
    except LookupError:
        return render(request, "customs_general/model_not_found.html", {"model": model})

    # Kullanıcı dostu model ismi ve ikon belirleme
    model_display_name = model_class._meta.verbose_name
    model_icon = MODEL_ICONS.get(model, "❓")

    # Arama işlemi
    query = request.GET.get("q", "").strip()  # Kullanıcıdan gelen arama terimi
    objects = model_class.objects.all()  # Varsayılan olarak tüm kayıtları getiriyoruz

    if query:
        search_filters = Q()
        for field in model_class._meta.fields:
            if field.get_internal_type() in ["CharField", "TextField"]:
                search_filters |= Q(**{f"{field.name}__icontains": query})  # Case-insensitive arama

        objects = objects.filter(search_filters)

    # Kullanıcının belirlediği sayfa başına gösterilecek veri miktarını al
    per_page = request.GET.get("per_page", 10)  # Varsayılan olarak 10 değer göster
    try:
        per_page = int(per_page) if int(per_page) in [10, 25, 50, 100] else 10
    except ValueError:
        per_page = 10  # Geçersiz giriş olursa varsayılan 10

    # Sayfalama işlemi
    paginator = Paginator(objects, per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Modelin field bilgilerini al
    field_names = [field.verbose_name for field in model_class._meta.fields]
    field_keys = [field.name for field in model_class._meta.fields]

    return render(request, "customs_general/model_data.html", {
        "model": model,
        "model_display_name": model_display_name,
        "model_icon": model_icon,
        "page_obj": page_obj,  # Sayfalama nesnesini template'e gönder
        "field_names": field_names,
        "field_keys": field_keys,
        "query": query,  # Arama kutusuna girilen değerin korunması için
        "per_page": per_page,  # Sayfa başına gösterilecek öğe sayısı
    })


@staff_member_required
def upload_excel(request, model):
    print(f"upload_excel fonksiyonu çağrıldı! Model: {model}")

    try:
        model_class = apps.get_model("customs_general", model)
        print(f"{model} modeli bulundu!")

        if request.method == "POST":
            print("POST isteği alındı!")

            if "excel_file" not in request.FILES:
                print("Hata: Excel dosyası yüklenmedi!")
                return JsonResponse({"success": False, "error": "Excel dosyası yüklenmedi!"})

            excel_file = request.FILES["excel_file"]
            print(f"Yüklenen dosya: {excel_file.name}")

            try:
                # Excel veya CSV dosyasını okuma
                if excel_file.name.endswith(".csv"):
                    df = pd.read_csv(excel_file)
                    print("CSV dosyası okundu.")
                elif excel_file.name.endswith(".xlsx"):
                    df = pd.read_excel(excel_file, engine="openpyxl")
                    print("XLSX dosyası okundu.")
                else:
                    print("Hata: Geçersiz dosya formatı!")
                    return JsonResponse({"success": False, "error": "Sadece .csv ve .xlsx dosyaları kabul edilir."})

                # Modelin field isimlerini al (id hariç)
                field_names = [field.name for field in model_class._meta.fields if field.name != "id"]
                print(f"Model field'ları: {field_names}")

                # Excel dosyasındaki kolon isimlerini doğrula
                for column in df.columns:
                    if column not in field_names:
                        print(f"Hata: Geçersiz sütun - {column}")
                        return JsonResponse(
                            {"success": False, "error": f"Geçersiz sütun: {column}. Beklenen sütunlar: {field_names}"})

                # Verileri veritabanına ekleme işlemi
                new_objects = []
                for _, row in df.iterrows():
                    obj_data = {field: row[field] for field in field_names}
                    new_objects.append(model_class(**obj_data))

                model_class.objects.bulk_create(new_objects)
                print(f"{len(new_objects)} kayıt eklendi!")

                return JsonResponse({"success": True, "message": f"{len(new_objects)} kayıt başarıyla eklendi!"})

            except Exception as e:
                print(f"Hata oluştu: {str(e)}")
                return JsonResponse({"success": False, "error": str(e)})

        else:
            return JsonResponse({"success": False, "error": "Sadece POST istekleri kabul edilir!"})

    except Exception as e:
        print(f"Genel Hata: {e}")
        return JsonResponse({"success": False, "error": str(e)})
