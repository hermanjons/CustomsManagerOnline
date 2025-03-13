from django.shortcuts import render, get_list_or_404
from django.apps import apps

from django.shortcuts import render, get_list_or_404
from django.apps import apps


def dashboard_home(request):
    # customs_general içindeki tüm modelleri al
    models = apps.get_app_config('customs_general').get_models()

    # Model isimlerini doğrudan almak için güncellendi (s eklenmeyecek)
    model_names = [model._meta.object_name for model in models]
    print(model_names)
    return render(request, 'dashboard/index.html', {'model_names': model_names})
