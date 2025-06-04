from django.shortcuts import render
from django.apps import apps
from core.views.mixins import RoleRequiredMixin
from django.views.generic import TemplateView


class DashboardHomeView(RoleRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    allowed_roles = ["client", "consultant", "admin"]
