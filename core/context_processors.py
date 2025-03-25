from django.apps import apps
from customs_general.constants import MODEL_ICONS  # MODEL_ICONS sabitlerinizi tanımladığınız dosyadan import edin


def model_list(request):
    """
    İki farklı uygulamadan modelleri çekip context'e ekler.

    - "customs_general" uygulamasına bağlı modeller, genel tanımlamalar altında listelenecek.
    - "product" uygulamasına bağlı modeller, ürün işlemleri altında listelenecek.
    """
    genel_tanimlamalar_models = []
    urun_islemleri_models = []

    for app_config in apps.get_app_configs():
        # "customs_general" uygulamasına ait modelleri alıyoruz.
        if app_config.label == 'customs_general':
            for model in app_config.get_models():
                model_name = model._meta.model_name
                icon = MODEL_ICONS.get(model_name, "❓")
                genel_tanimlamalar_models.append({
                    "model": model_name,
                    "display_name": model._meta.verbose_name,
                    "icon": icon,
                })
        # "product" uygulamasına ait modelleri alıyoruz.
        elif app_config.label == 'products':
            for model in app_config.get_models():
                model_name = model._meta.model_name
                icon = MODEL_ICONS.get(model_name, "❓")
                urun_islemleri_models.append({
                    "model": model_name,
                    "display_name": model._meta.verbose_name,
                    "icon": icon,
                })

    return {
        "genel_tanimlamalar_models": genel_tanimlamalar_models,
        "urun_islemleri_models": urun_islemleri_models,
    }
