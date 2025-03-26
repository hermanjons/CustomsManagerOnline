from django.apps import apps
from core.constants import MODEL_ICONS  # MODEL_ICONS sabitlerinizi tanımladığınız dosyadan import edin
from django.conf import settings
from django.templatetags.static import static


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


# Eğer SiteSettings gibi dinamik bir modeliniz varsa, onu da kullanabilirsiniz.

def site_logo_release(request):
    """
    Site logosunu template'lere aktarır.
    Eğer dinamik bir ayar modeliniz varsa, ondan çekebilir ya da settings üzerinden statik olarak tanımlayabilirsiniz.
    """
    # Örneğin, settings.py içinde SITE_LOGO tanımlıysa:
    if hasattr(settings, 'SITE_LOGO') and settings.SITE_LOGO:
        site_logo = settings.SITE_LOGO  # Bu, logo URL'si veya dosya nesnesi olabilir
        print(site_logo)
    else:
        # Varsayılan logo için static dosya yolunu kullanıyoruz:
        site_logo = static('/media/onlinecustoms.png')

    return {'site_logo': site_logo}
