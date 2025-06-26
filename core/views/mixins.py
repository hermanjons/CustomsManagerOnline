# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from accounts.models import ClientProfile
from django.apps import apps
from django.shortcuts import render


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    @property
    def effective_allowed_roles(self):
        """
        allowed_roles + admin her zaman erişebilir → otomatik olarak admin'i de ekleriz.
        Böylece view'larda 'admin' yazmak zorunda kalmayız.
        """
        return self.allowed_roles + ['admin'] if 'admin' not in self.allowed_roles else self.allowed_roles

    def test_func(self):
        user = self.request.user

        # 0️⃣ Eğer admin ise → direkt izin ver → diğer kontrolleri atla.
        if user.role == "admin":
            return True

        # 1️⃣ Role kontrolü (admin dışındaki roller için geçerli)
        if not (user.is_authenticated and user.role in self.allowed_roles):
            return False

        # 2️⃣ Eğer müşavir ise → aktif müşteri seçimine göre yetki kontrolü yapılır
        if user.role == "consultant":
            active_client_id = self.request.session.get("active_client_id")
            if active_client_id:
                try:
                    client = ClientProfile.objects.get(id=active_client_id)
                    return client in user.consulted_clients.all()
                except ClientProfile.DoesNotExist:
                    return False
            else:
                return True  # Aktif seçim istenmiyorsa → giriş serbest

        # 3️⃣ Eğer müşteri ise → aktif müşavir seçimine göre yetki kontrolü yapılır
        elif user.role == "client":
            active_consultant_id = self.request.session.get("active_consultant_id")
            if active_consultant_id:
                client_profile = getattr(user, "client_profile", None)
                if client_profile:
                    return client_profile.consultants.filter(id=active_consultant_id).exists()
                else:
                    return False
            else:
                return True

    def handle_no_permission(self):
        raise PermissionDenied("Bu sayfaya erişim yetkiniz yok.")


class DynamicModelLoaderMixin:
    """
    URL'den veya GET parametresinden model ismini okuyarak
    self.model üzerine atan dinamik model yükleyici mixin.
    """

    app_label = None  # View'de mutlaka tanımlanmalı
    model_param = "model"  # URL veya GET parametresinde model ismi beklenen parametre adı

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get(self.model_param) or request.GET.get(self.model_param)
        try:
            self.model = apps.get_model(self.app_label, model_name)
        except LookupError:
            return render(request, "model_not_found.html", {"model": model_name})
        return super().dispatch(request, *args, **kwargs)



class RoleBasedAccessMixin:
    client_field_in_model = "created_by"

    def get_queryset(self):
        user = self.request.user
        print("kullanıcı")
        if user.role == "client":
            return self.model.objects.filter(**{self.client_field_in_model: user})

        elif user.role == "consultant":
            print("müşavir")
            active_client_id = self.request.session.get("active_client_id")
            if active_client_id:
                try:
                    client = ClientProfile.objects.get(id=active_client_id)
                    if client in user.consulted_clients.all():
                        return self.model.objects.filter(**{self.client_field_in_model: client.user})
                except ClientProfile.DoesNotExist:
                    pass
            return self.model.objects.none()

        return self.model.objects.filter()



class DetailViewMixin:
    def get(self, request, *args, **kwargs):
        if request.GET.get("detail") == "1":
            pk = kwargs.get("pk")
            return self.get_object_detail_json(pk)
        return super().get(request, *args, **kwargs)
