from django.apps import apps
from django.shortcuts import render
from core.views.views import GenericFilteredListView
from core.views.mixins import RoleRequiredMixin


class GeneralCustomsModelListView(RoleRequiredMixin, GenericFilteredListView):
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

    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get(self.model_param) or request.GET.get(self.model_param)
        try:
            self.model = apps.get_model(self.app_label, model_name)
        except LookupError:
            return render(request, "model_not_found.html", {"model": model_name})
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        if request.GET.get("detail") == "1":

            pk = kwargs.get("pk")
            return self.get_object_detail_json(pk)
        else:
            print(request.GET)

        return super().get(request, *args, **kwargs)
