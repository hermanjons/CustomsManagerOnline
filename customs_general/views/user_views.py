from django.apps import apps
from django.shortcuts import render
from core.views.views import GenericFilteredListView
from core.views.mixins import RoleBasedAccessMixin, DetailViewMixin, DynamicModelLoaderMixin, RoleRequiredMixin


class GeneralCustomsModelListView(RoleRequiredMixin, DetailViewMixin, DynamicModelLoaderMixin,
                                  GenericFilteredListView):
    """
    customs_general uygulamasındaki tanım modellerini listelemek için
    dinamik olarak çalışan generic view sınıfı.
    """
    app_label = "customs_general"
    model_param = "model"
    template_name = "customs_general/customs_general_page.html"
    excluded_fields = ["is_active", "is_global", "id", "created_at", "updated_at",
                       "updated_by", "created_by", "record_uuid", "system_note"]
    allowed_roles = ["consultant", "admin"]  # Kimler görebilir?
