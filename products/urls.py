from django.urls import path
from .views import brand_page_view,BrandCreateView

app_label = "products"

urlpatterns = [
    path('brands/', brand_page_view, name='brand_page_view'),
    path('brand/create/', BrandCreateView.as_view(), name='brand_create'),
]
