from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.contrib import admin
from django.apps import apps


class CustomAdmin(admin.ModelAdmin):
    change_list_template = "admin/excel_upload.html"

    def get_autocomplete_fields(self, request):
        """ForeignKey ve ManyToMany alanları otomatik autocomplete yap."""
        autocomplete = []
        for field in self.model._meta.fields:
            if field.get_internal_type() == 'ForeignKey':
                autocomplete.append(field.name)
        for m2m_field in self.model._meta.many_to_many:
            autocomplete.append(m2m_field.name)
        return autocomplete

    def get_raw_id_fields(self, request):
        """Gerekirse burada raw_id_fields ekleyebiliriz. Şu an boş."""
        return []

    def get_search_fields(self, request):
        """Modeldeki tüm CharField ve TextField alanları search_fields olarak ayarla."""
        search_fields = []
        for field in self.model._meta.fields:
            if field.get_internal_type() in ['CharField', 'TextField']:
                search_fields.append(field.name)
        return search_fields

    def get_form(self, request, obj=None, **kwargs):
        self.autocomplete_fields = self.get_autocomplete_fields(request)
        self.raw_id_fields = self.get_raw_id_fields(request)
        self.search_fields = self.get_search_fields(request)

        form = super().get_form(request, obj, **kwargs)

        # 🔥 Sadece PaymentMethod için ve bağlı olduğu DataSource global ise muadil alanı gizle
        if self.model.__name__ == "PaymentMethod" and obj:
            if getattr(obj.data_source, "is_global", False):
                if "standard_reference" in form.base_fields:
                    form.base_fields.pop("standard_reference")

        return form

    def changelist_view(self, request, extra_context=None):
        if extra_context is None:
            extra_context = {}
        default_context = self.admin_site.each_context(request)
        extra_context = {**default_context, **extra_context}

        model_name = self.model._meta.model_name
        try:
            upload_excel_url = reverse(f'admin:admin_upload_excel_{model_name}')
        except Exception:
            upload_excel_url = "#"

        extra_context['upload_excel_button'] = mark_safe(
            f'<a href="{upload_excel_url}" class="button" style="margin-bottom:10px; background:green; color:white; padding:10px; border-radius:5px;">📤 Excel ile Yükle</a>'
        )
        extra_context['model_name'] = model_name

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        model_name = self.model._meta.model_name

        custom_urls = [
            path(
                f'upload-excel/',
                self.redirect_to_upload_excel,
                name=f'admin_upload_excel_{model_name}'
            ),
        ]
        return custom_urls + urls

    def redirect_to_upload_excel(self, request):
        model_name = self.model._meta.model_name
        return redirect(reverse("customs_general:upload_excel", args=[model_name]))


# MODELLERİ TOPLU KAYDEDİYORSAN AŞAĞIDAKİ DE VAR:
models = apps.get_app_config("customs_general").get_models()

for model in models:
    admin.site.register(model, CustomAdmin)
