from django.apps import apps
from .constants import MODEL_ICONS


def model_list(request):
    """Tüm modelleri UI dostu isimleri ve Twemoji ikonlarıyla birlikte template'e gönderir."""
    models = apps.get_app_config("customs_general").get_models()
    model_names = []

    for model in models:
        model_name = model._meta.model_name
        icon = MODEL_ICONS.get(model_name, "❓")  # Eğer `MODEL_ICONS` içinde yoksa varsayılan ikon ata
        model_names.append({
            "model": model_name,
            "display_name": model._meta.verbose_name,  # Kullanıcı dostu model ismi
            "icon": icon,  # Twemoji bilgisi artık constants.py'den çekiliyor!
        })

    return {"models": model_names}
