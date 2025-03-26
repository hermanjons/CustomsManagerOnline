from django.urls import path
from .views import brand_page_view, BrandCreateView, model_page_view

app_label = "products"

urlpatterns = [
    path('brands/', brand_page_view, name='brand_page_view'),
    path('brands/create/', BrandCreateView.as_view(), name='brand_create'),
    path('models/', model_page_view, name ='model_page_view')
]
