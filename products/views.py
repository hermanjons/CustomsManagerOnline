from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from .models import Brand, ProductModel, Products, UploadedDocuments
from customs_general.models import TaxCode, GtipCode
from .forms import BrandForm, ProductModelForm, ProductsForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from core.utils import GenericFilteredListView, AjaxFilteredListView
from django.http import JsonResponse
from django.db.models import Q


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
    context_object_name = 'models'


class ProductsListView(GenericFilteredListView):
    model = Products
    template_name = 'products/products_page.html'
    context_object_name = 'products'


class ProductsCreateView(CreateView):
    model = Products
    form_class = ProductsForm
    template_name = 'products/products_create.html'
    success_url = reverse_lazy('products_page_view')


class UploadedDocsListView(GenericFilteredListView):
    model = UploadedDocuments
    template_name = 'products/uploaded_docs_page.html'
    context_object_name = 'uploaded_documents'


class UploadedDocsModalSearch(AjaxFilteredListView):
    model = UploadedDocuments
    search_fields = ['doc_name']  # sadece doc_name üzerinden arama yapsın


def tax_code_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        matched = TaxCode.objects.filter(name__icontains=query)[:20]
        results = [
            {"id": t.id, "code": t.code, "name": t.name}
            for t in matched
        ]
    return JsonResponse({"results": results})


def gtip_code_search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        matches = GtipCode.objects.filter(
            Q(code__icontains=query) | Q(desc__icontains=query)
        )[:20]
        results = [{"id": g.id, "code": g.code, "name": g.desc} for g in matches]
    return JsonResponse({"results": results})
