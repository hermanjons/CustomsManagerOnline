from .models import Brand, ProductModel, Products, UploadedDocuments
from customs_general.models import TaxCode, GtipCode
from .forms import BrandForm, ProductModelForm, ProductsForm, UploadedDocsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.views.views import GenericFilteredListView, AjaxFilteredListView
from core.views.mixins import RoleRequiredMixin
from accounts.models import ClientProfile


class RoleBasedListView(RoleRequiredMixin, GenericFilteredListView):
    client_field_in_model = "created_by"  # Modelde client'i tutan field adı (default olarak created_by)

    def get_queryset(self):
        user = self.request.user

        # Eğer kullanıcı müşteri ise sadece kendi ürünlerini/nesnelerini görür
        if user.role == "client":
            return self.model.objects.filter(**{self.client_field_in_model: user})

        # Eğer kullanıcı müşavir ise ve bir müşteri seçmişse
        elif user.role == "consultant":
            print("rol: müşavir ")
            active_client_id = self.request.session.get("active_client_id")
            print("aktif müşterinin id değeri (session'dan):", active_client_id)

            if active_client_id:
                try:
                    client = ClientProfile.objects.get(id=active_client_id)

                    # Bu müşteri gerçekten bu müşavirin müşterisi mi?
                    if client in user.consulted_clients.all():
                        return self.model.objects.filter(**{self.client_field_in_model: client.user})
                except ClientProfile.DoesNotExist:
                    pass

            return self.model.objects.none()



class BrandCreateView(RoleRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_create.html'
    success_url = reverse_lazy('brand_page_view')
    allowed_roles = ["client", "consultant"]


class ProductModelCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["client", "consultant"]
    model = ProductModel
    form_class = ProductModelForm
    template_name = 'products/model_create.html'
    success_url = reverse_lazy('model_page_view')



class BrandListView(RoleBasedListView):
    model = Brand
    template_name = 'products/brand_page.html'
    context_object_name = 'brands'
    allowed_roles = ["client", "consultant"]


class ProductModelListView(RoleBasedListView):
    model = ProductModel
    template_name = 'products/model_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'models'
    allowed_roles = ["client", "consultant"]


class ProductsListView(RoleBasedListView):
    model = Products
    template_name = 'products/products_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'products'
    allowed_roles = ["client", "consultant"]




class ProductsCreateView(RoleRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'products/products_create.html'
    success_url = reverse_lazy('products_page_view')
    allowed_roles = ["client", "consultant"]

    def form_valid(self, form):
        response = super().form_valid(form)

        tax_codes = self.request.POST.getlist('tax_codes[]')
        documents = self.request.POST.getlist('documents[]')

        if tax_codes:
            self.object.tax_code.set(tax_codes)

        if documents:
            self.object.doc_name.set(documents)  # Çoklu belge ilişkisi (ManyToMany)

        return response


class UploadedDocsListView(RoleBasedListView):
    model = UploadedDocuments
    template_name = 'products/uploaded_docs_page.html'
    context_object_name = 'uploaded_documents'
    allowed_roles = ["client", "consultant"]


class UploadedDocsCreateView(RoleRequiredMixin, CreateView):
    model = UploadedDocuments
    form_class = UploadedDocsForm
    template_name = 'products/uploaded_docs_create.html'
    success_url = reverse_lazy('uploaded_docs_view')
    allowed_roles = ["client", "consultant"]


class UploadedDocsModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = UploadedDocuments
    search_fields = ['doc_name']  # sadece doc_name üzerinden arama yapsın
    allowed_roles = ["client", "consultant"]


class TaxCodeModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = TaxCode
    allowed_roles = ["client", "consultant"]


class GtipCodeModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = GtipCode
    allowed_roles = ["client", "consultant"]
