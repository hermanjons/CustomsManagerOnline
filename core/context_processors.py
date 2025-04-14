from django.apps import apps
from core.constants import MODEL_ICONS, \
    MODEL_FIELD_VERBOSE_NAMES  # MODEL_ICONS sabitlerinizi tanımladığınız dosyadan import edin
from django.conf import settings
from django.templatetags.static import static


DIGER_MODELLER = ['transactiontype', 'additionalinfocode', 'antidumpingcompany','chiefcustomsoffice',
                  'transportvehicle', 'internationalagreement', 'simplifiedprocedure', 'harbor', 'exemptioncode',
                  'airlinecompany', 'regimecode', 'warehouse']


def model_list(request):
    """
    Uygulamalardan modelleri çekip context'e ekler:
    - "customs_general" uygulamasına ait modeller: genel_tanimlamalar altında
    - "products" uygulamasına ait modeller: ürün işlemleri altında
    - Belirli modeller: "diğer" başlığı altında
    """

    genel_tanimlamalar_models = []
    urun_islemleri_models = []
    diger_models = []

    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            model_name = model._meta.model_name
            icon = MODEL_ICONS.get(model_name, "❓")
            item = {
                "model": model_name,
                "display_name": model._meta.verbose_name,
                "icon": icon,
            }

            # Eğer model diğer grubuna aitse
            if model_name in DIGER_MODELLER:
                diger_models.append(item)
            elif app_config.label == 'customs_general':
                genel_tanimlamalar_models.append(item)
            elif app_config.label == 'products':
                urun_islemleri_models.append(item)

    return {
        "genel_tanimlamalar_models": genel_tanimlamalar_models,
        "urun_islemleri_models": urun_islemleri_models,
        "diger_models": diger_models,
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


def model_field_verbose_names(request):
    return {'model_field_verbose_names': MODEL_FIELD_VERBOSE_NAMES}
