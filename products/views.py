from .models import Brand, ProductModel, Products, UploadedDocuments
from customs_general.models import TaxCode, GtipCode
from .forms import BrandForm, ProductModelForm, ProductsForm, UploadedDocsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.views import GenericFilteredListView, AjaxFilteredListView


class BrandCreateView(CreateView):
    model = Brand
    form_class = BrandForm
    template_name = 'products/brand_create.html'
    success_url = reverse_lazy('brand_page_view')


class ProductModelCreateView(CreateView):
    model = ProductModel
    form_class = ProductModelForm
    template_name = 'products/model_create.html'
    success_url = reverse_lazy('model_page_view')


class BrandListView(GenericFilteredListView):
    model = Brand
    template_name = 'products/brand_page.html'
    context_object_name = 'brands'


class ProductModelListView(GenericFilteredListView):
    model = ProductModel
    template_name = 'products/model_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'models'


class ProductsListView(GenericFilteredListView):
    model = Products
    template_name = 'products/products_page.html'
    related_search_fields = ["brand__brand_name"]
    context_object_name = 'products'


class ProductsCreateView(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'products/products_create.html'
    success_url = reverse_lazy('products_page_view')

    def form_valid(self, form):
        response = super().form_valid(form)

        tax_codes = self.request.POST.getlist('tax_codes[]')
        documents = self.request.POST.getlist('documents[]')

        if tax_codes:
            self.object.tax_code.set(tax_codes)

        if documents:
            self.object.doc_name.set(documents)  # Çoklu belge ilişkisi (ManyToMany)

        return response


class UploadedDocsListView(GenericFilteredListView):
    model = UploadedDocuments
    template_name = 'products/uploaded_docs_page.html'
    context_object_name = 'uploaded_documents'


class UploadedDocsCreateView(CreateView):
    model = UploadedDocuments
    form_class = UploadedDocsForm
    template_name = 'products/uploaded_docs_create.html'
    success_url = reverse_lazy('uploaded_docs_view')


class UploadedDocsModalSearch(AjaxFilteredListView):
    model = UploadedDocuments
    search_fields = ['doc_name']  # sadece doc_name üzerinden arama yapsın


class TaxCodeModalSearch(AjaxFilteredListView):
    model = TaxCode


class GtipCodeModalSearch(AjaxFilteredListView):
    model = GtipCode
