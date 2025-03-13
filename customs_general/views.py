from django.shortcuts import render, redirect
from django.apps import apps
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.contrib import messages, admin
from django.contrib.admin.views.decorators import staff_member_required


def model_data(request, model):
    try:
        model_class = apps.get_model('customs_general', model)
    except LookupError:
        return render(request, 'customs_general/model_not_found.html', {'model': model})

    objects = model_class.objects.all()
    field_names = [field.verbose_name for field in model_class._meta.fields]
    field_keys = [field.name for field in model_class._meta.fields]

    # Tüm modelleri tekrar alarak model_names değişkenini ekleyelim
    models = apps.get_app_config('customs_general').get_models()
    model_names = [model._meta.object_name for model in models]

    return render(request, 'customs_general/model_data.html', {
        'model': model,
        'objects': objects,
        'field_names': field_names,
        'field_keys': field_keys,
        'model_names': model_names,  # Model isimlerini template'e ekledik
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
                        return JsonResponse({"success": False, "error": f"Geçersiz sütun: {column}. Beklenen sütunlar: {field_names}"})

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
