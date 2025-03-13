from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
from django.contrib import admin
from django.apps import apps


class CustomAdmin(admin.ModelAdmin):
    change_list_template = "admin/excel_upload.html"

    def changelist_view(self, request, extra_context=None):
        # Eğer extra_context yoksa oluşturuyoruz
        if extra_context is None:
            extra_context = {}
        # Django admin’in varsayılan context’ini de alıyoruz
        default_context = self.admin_site.each_context(request)
        extra_context = {**default_context, **extra_context}

        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        print(f"Model: {model_name} | App Label: {app_label}")

        try:
            upload_excel_url = reverse('admin:admin_upload_excel', args=[model_name])
            print(f"Oluşturulan Excel URL'si: {upload_excel_url}")
        except Exception as e:
            print(f"URL oluşturulurken hata oluştu: {e}")
            upload_excel_url = "#"  # Hata durumunda güvenli redirect

        # Excel ile Yükle butonunu oluşturuyoruz
        extra_context['upload_excel_button'] = mark_safe(
            f'<a href="{upload_excel_url}" class="button" style="margin-bottom:10px; background:green; color:white; padding:10px; border-radius:5px;">📤 Excel ile Yükle</a>'
        )
        extra_context['model_name'] = model_name

        # Şablon içinde kullanılan app_label ve opts bilgilerini sağlıyoruz
        extra_context['app_label'] = app_label if app_label else "customs_general"
        extra_context['opts'] = self.model._meta

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/<str:model>/', self.redirect_to_upload_excel, name="admin_upload_excel"),
        ]
        return custom_urls + urls

    def redirect_to_upload_excel(self, request, model):
        return redirect(reverse('customs_general:upload_excel', args=[model]))


models = apps.get_app_config("customs_general").get_models()

# Her modeli `CustomAdmin` ile admin paneline kaydet
for model in models:
    admin.site.register(model, CustomAdmin)
