from django.shortcuts import render, get_list_or_404
from django.apps import apps

from django.shortcuts import render, get_list_or_404
from django.apps import apps


def dashboard_home(request):
    # customs_general içindeki tüm modelleri al
    models = apps.get_app_config('customs_general').get_models()

    # Model isimlerini doğrudan almak için güncellendi (s eklenmeyecek)
    model_names = [model._meta.object_name for model in models]

    return render(request, 'dashboard/index.html', {'model_names': model_names})


def model_data(request, model):
    try:
        model_class = apps.get_model('customs_general', model)
    except LookupError:
        return render(request, 'dashboard/model_not_found.html', {'model': model})

    # Tüm nesneleri al
    objects = model_class.objects.all()

    # Alan isimleri ve field adlarını birlikte al
    field_names = [field.verbose_name for field in model_class._meta.fields]
    field_keys = [field.name for field in model_class._meta.fields]  # Alanların teknik adları

    return render(request, 'dashboard/model_data.html', {
        'model': model,
        'objects': objects,
        'field_names': field_names,
        'field_keys': field_keys,  # Alan isimleri için ayrı key listesi
    })
