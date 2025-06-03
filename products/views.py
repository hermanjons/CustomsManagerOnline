from .models import Brand, ProductModel, Products, UploadedDocuments
from customs_general.models import TaxCode, GtipCode
from .forms import BrandForm, ProductModelForm, ProductsForm, UploadedDocsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.views.views import GenericFilteredListView, AjaxFilteredListView
from core.views.mixins import RoleRequiredMixin


class BrandCreateView(RoleRequiredMixin, CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_create.html'
    success_url = reverse_lazy('brand_page_view')
    allowed_roles = ["client"]


class ProductModelCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ["client"]
    model = ProductModel
    form_class = ProductModelForm
    template_name = 'products/model_create.html'
    success_url = reverse_lazy('model_page_view')



class BrandListView(RoleRequiredMixin, GenericFilteredListView):
    model = Brand
    template_name = 'products/brand_page.html'
    context_object_name = 'brands'
    allowed_roles = ["client"]


class ProductModelListView(RoleRequiredMixin, GenericFilteredListView):
    model = ProductModel
    template_name = 'products/model_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'models'
    allowed_roles = ["client"]


class ProductsListView(RoleRequiredMixin, GenericFilteredListView):
    model = Products
    template_name = 'products/products_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'products'
    allowed_roles = ["client"]


class ProductsCreateView(RoleRequiredMixin, CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'products/products_create.html'
    success_url = reverse_lazy('products_page_view')
    allowed_roles = ["client"]

    def form_valid(self, form):
        response = super().form_valid(form)

        tax_codes = self.request.POST.getlist('tax_codes[]')
        documents = self.request.POST.getlist('documents[]')

        if tax_codes:
            self.object.tax_code.set(tax_codes)

        if documents:
            self.object.doc_name.set(documents)  # Çoklu belge ilişkisi (ManyToMany)

        return response


class UploadedDocsListView(RoleRequiredMixin, GenericFilteredListView):
    model = UploadedDocuments
    template_name = 'products/uploaded_docs_page.html'
    context_object_name = 'uploaded_documents'
    allowed_roles = ["client"]


class UploadedDocsCreateView(RoleRequiredMixin, CreateView):
    model = UploadedDocuments
    form_class = UploadedDocsForm
    template_name = 'products/uploaded_docs_create.html'
    success_url = reverse_lazy('uploaded_docs_view')
    allowed_roles = ["client"]


class UploadedDocsModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = UploadedDocuments
    search_fields = ['doc_name']  # sadece doc_name üzerinden arama yapsın
    allowed_roles = ["client"]


class TaxCodeModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = TaxCode
    allowed_roles = ["client"]


class GtipCodeModalSearch(RoleRequiredMixin, AjaxFilteredListView):
    model = GtipCode
    allowed_roles = ["client"]
