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
        # sözlükleri birleştirdik
        extra_context = {**default_context, **extra_context}

        model_name = self.model._meta.model_name
        try:
            upload_excel_url = reverse(f'admin:admin_upload_excel_{model_name}')
        except Exception as e:
            upload_excel_url = "#"  # Hata durumunda güvenli redirect

        # Excel ile Yükle butonunu oluşturuyoruz
        extra_context['upload_excel_button'] = mark_safe(
            f'<a href="{upload_excel_url}" class="button" style="margin-bottom:10px; background:green; color:white; padding:10px; border-radius:5px;">📤 Excel ile Yükle</a>'
        )
        extra_context['model_name'] = model_name

        return super().changelist_view(request, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        model_name = self.model._meta.model_name  #Hangi modeldeyiz

        custom_urls = [
            path(
                f'upload-excel/',
                self.redirect_to_upload_excel,
                name=f'admin_upload_excel_{model_name}' #Benzersiz isim!
            ),
        ]
        return custom_urls + urls

    def redirect_to_upload_excel(self, request):
        model_name = self.model._meta.model_name
        return redirect(reverse("customs_general:upload_excel", args=[model_name]))


models = apps.get_app_config("customs_general").get_models()

# Her modeli `CustomAdmin` ile admin paneline kaydet
for model in models:

    admin.site.register(model, CustomAdmin)
