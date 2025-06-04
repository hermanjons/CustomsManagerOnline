from django.apps import apps
from core.constants import MODEL_ICONS, \
    MODEL_FIELD_VERBOSE_NAMES  # MODEL_ICONS sabitlerinizi tanımladığınız dosyadan import edin
from django.conf import settings
from django.templatetags.static import static
from .constants import ROLE_APP_BLACKLIST

from accounts.models import ClientProfile

DIGER_MODELLER = ['transactiontype', 'additionalinfocode', 'antidumpingcompany', 'chiefcustomsoffice',
                  'transportvehicle', 'internationalagreement', 'simplifiedprocedure', 'harbor', 'exemptioncode',
                  'airlinecompany', 'regimecode', 'warehouse']


def assigned_clients_context(request):
    user = request.user
    context = {}

    if user.is_authenticated and user.role == "consultant":
        # Sadece kendisini müşavir olarak kabul etmiş müşteriler
        assigned_clients = ClientProfile.objects.filter(consultants=user)
        context["assigned_clients"] = assigned_clients
        active_client_id = request.session.get("active_client_id")
        if active_client_id:
            context["active_client"] = assigned_clients.filter(id=active_client_id).first()

    return context


def model_list(request):
    """
    Uygulamalardan modelleri çekip context'e ekler:
    App bazlı rol filtrelemesi yapılır.
    """
    genel_tanimlamalar_models = []
    urun_islemleri_models = []
    diger_models = []
    user_role = getattr(request.user, "role", None)
    blacklisted_apps = ROLE_APP_BLACKLIST.get(user_role, [])
    for app_config in apps.get_app_configs():
        # App rol erişim filtresi
        if app_config.label in blacklisted_apps:
            print("geçildi")
            continue

        for model in app_config.get_models():
            model_name = model._meta.model_name
            icon = MODEL_ICONS.get(model_name, "❓")
            item = {
                "model": model_name,
                "display_name": model._meta.verbose_name,
                "icon": icon,
            }

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
    if hasattr(settings, 'SITE_LOGO') and settings.SITE_LOGO:
        site_logo = static(settings.SITE_LOGO)
    else:
        # STATIC kullanarak yol veriyoruz
        site_logo = static('onlinecustoms.png')
    return {'site_logo': site_logo}


def user_role(request):
    if request.user.is_authenticated:
        return {"user_role": request.user.role}
    return {}
