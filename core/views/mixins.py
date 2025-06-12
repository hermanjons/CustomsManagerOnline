# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from accounts.models import ClientProfile


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user

        # 1️⃣ Role kontrolü
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

