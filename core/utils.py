import os
from datetime import datetime
from django.views.generic import ListView

from django.db.models import Q, TextField, CharField, ForeignKey, ManyToManyField
from django.http import response, JsonResponse


def date_based_upload_path(instance, filename):
    """
    Dosyaları, 'uploads/YYYY/MM/DD/' yapısına göre kaydeder ve
    dosya adını tarih-saat bilgisi ile benzersiz hale getirir.
    """
    ext = filename.split('.')[-1]
    new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('uploads', datetime.now().strftime('%Y/%m/%d'), new_filename)


class GenericFilteredListView(ListView):
    query_param = 'q'
    search_fields = None
    related_search_fields = None
    paginate_by_default = 10

    def get_search_fields(self):
        if self.search_fields is not None:
            return self.search_fields

        # search_fields verilmemişse tüm non-relation CharField ve TextField alanları otomatik al
        return [
            field.name
            for field in self.model._meta.get_fields()
            if isinstance(field, (CharField, TextField)) and not field.is_relation
        ]

    def get_related_search_fields(self):
        if self.related_search_fields is not None:
            return self.related_search_fields

        # related_search_fields verilmemişse hiç relation alanı aranmayacak
        return []

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get(self.query_param, '').strip()

        if query:
            q_obj = Q()

            # Normal alanlar için arama
            for field in self.get_search_fields():
                q_obj |= Q(**{f"{field}__icontains": query})

            # Related alanlar için arama
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


class AjaxFilteredListView(GenericFilteredListView):
    def render_to_response(self, context, **response_kwargs):
        # queryset'teki verileri JSON'a çevir
        data = list(context['object_list'].values())
        print(data)
        return JsonResponse({'results': data})
