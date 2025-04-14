from django.urls import path
from .views import BrandCreateView, ProductModelCreateView, BrandListView, ProductModelListView, ProductsListView,\
    ProductsCreateView, GtipCodeModalSearch, TaxCodeModalSearch, UploadedDocsListView, UploadedDocsModalSearch,\
    UploadedDocsCreateView

app_label = "products"

urlpatterns = [
    path('brands/', BrandListView.as_view(), name='brand_page_view'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('models/', ProductModelListView.as_view(), name='model_page_view'),
    path('models/create/', ProductModelCreateView.as_view(), name="model_create"),
    path('products/', ProductsListView.as_view(), name='products_page_view'),
    path('products/create/', ProductsCreateView.as_view(), name='products_create'),
    path('uploadeddocs/', UploadedDocsListView.as_view(), name='uploaded_docs_view'),
    path('ajax/tax-code-search/', TaxCodeModalSearch.as_view(), name='tax_code_search'),
    path('ajax/gtip-code-search/', GtipCodeModalSearch.as_view(), name='gtip_code_search'),
    path('ajax/document-search/', UploadedDocsModalSearch.as_view(), name='document_search'),
    path('uploadeddocs/create/', UploadedDocsCreateView.as_view(), name="uploaded_docs_create"),

]
