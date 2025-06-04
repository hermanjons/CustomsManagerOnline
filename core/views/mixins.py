# core/mixins.py
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(UserPassesTestMixin):
    allowed_roles = []

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in self.allowed_roles

    def handle_no_permission(self):
        raise PermissionDenied("Bu sayfaya erişim yetkiniz yok.")
