from django.shortcuts import render

from django.views.generic import ListView

from django.db.models import Q, TextField, CharField, ForeignKey, ManyToManyField
from django.http import response, JsonResponse
from core.constants import MODEL_ICONS, MODEL_FIELD_VERBOSE_NAMES
from .mixins import RoleRequiredMixin


class GenericFilteredListView(ListView):
    model = None
    query_param = 'q'
    search_fields = None
    related_search_fields = None
    paginate_by_default = 10

    # NOT: visible_fields ve excluded_fields burada tanımlanmıyor
    # Çünkü her alt sınıf kendisi belirleyecek

    def get_search_fields(self):
        if self.search_fields is not None:
            return self.search_fields
        return [
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, (CharField, TextField)) and not field.is_relation
        ]

    def get_related_search_fields(self):
        return self.related_search_fields or []

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get(self.query_param, '').strip()

        if query:
            q_obj = Q()
            for field in self.get_search_fields():
                q_obj |= Q(**{f"{field}__icontains": query})
            for related_field in self.get_related_search_fields():
                q_obj |= Q(**{f"{related_field}__icontains": query})
            qs = qs.filter(q_obj)

        return qs

    def get_paginate_by(self, queryset):
        per_page = self.request.GET.get('per_page', self.paginate_by_default)
        try:
            return int(per_page)
        except (ValueError, TypeError):
            return self.paginate_by_default

    def get_visible_fields(self):
        # Öncelikli: visible_fields tanımlıysa sadece onları göster
        if hasattr(self, 'visible_fields') and self.visible_fields is not None:
            return [
                field for field in self.model._meta.fields
                if field.name in self.visible_fields
            ]
        # Aksi halde excluded_fields varsa onu dikkate al
        excluded = getattr(self, 'excluded_fields', [])
        return [
            field for field in self.model._meta.fields
            if field.name not in excluded
        ]

    def get_model_meta_context(self):
        model_name = self.model.__name__.lower()
        visible_fields = self.get_visible_fields()
        m2m_fields = list(self.model._meta.many_to_many)

        return {
            "model": model_name,
            "model_display_name": self.model._meta.verbose_name,
            "model_icon": MODEL_ICONS.get(model_name, "❓"),
            "field_keys": [field.name for field in visible_fields + m2m_fields],
            "model_field_verbose_names": MODEL_FIELD_VERBOSE_NAMES.get(model_name, {}),
            "m2m_fields": m2m_fields,  # field objeleri olarak
        }

    def get_model_meta_json(self):
        model_name = self.model.__name__.lower()
        visible_fields = self.get_visible_fields()
        m2m_fields = list(self.model._meta.many_to_many)

        return {
            "model": model_name,
            "model_display_name": self.model._meta.verbose_name,
            "model_icon": MODEL_ICONS.get(model_name, "❓"),
            "field_keys": [field.name for field in visible_fields + m2m_fields],
            "model_field_verbose_names": MODEL_FIELD_VERBOSE_NAMES.get(model_name, {}),
            "m2m_field_names": [field.name for field in m2m_fields],
        }

    def get_object_detail_json(self, pk):
        try:
            obj = self.model.objects.get(pk=pk)
            meta_context = self.get_model_meta_json()

            data = {}

            for field_name in meta_context["field_keys"]:
                raw_value = getattr(obj, field_name, None)

                if field_name in meta_context["m2m_field_names"]:
                    items = raw_value.all() if raw_value else []
                    value = ", ".join(str(item) for item in items) if items else "-"
                else:
                    value = str(raw_value) if raw_value not in [None, ""] else "-"

                data[field_name] = value

            return JsonResponse({**meta_context, "data": data})

        except self.model.DoesNotExist:
            return JsonResponse({'error': 'Kayıt bulunamadı'}, status=404)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_model_meta_context())
        context.update({
            "query": self.request.GET.get(self.query_param, ""),
            "per_page": self.get_paginate_by(self.get_queryset()),
        })
        return context


class AjaxFilteredListView(GenericFilteredListView):
    def render_to_response(self, context, **response_kwargs):
        # queryset'teki verileri JSON'a çevir
        data = list(context['object_list'].values())
        return JsonResponse({'results': data})

