from .constants import MODEL_DISPLAY_NAMES, MODEL_ICONS
from django.apps import apps


def model_list(request):
    models = apps.get_app_config("customs_general").get_models()
    model_names = [
        {
            "model": model._meta.model_name,
            "display_name": MODEL_DISPLAY_NAMES.get(model._meta.model_name, model._meta.verbose_name),
            "icon": MODEL_ICONS.get(model._meta.model_name, "fas fa-question-circle"),
        }
        for model in models
    ]
    return {"models": model_names}
