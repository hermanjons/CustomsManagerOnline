from django import forms
from .models import Brand, ProductModel, Products, UploadedDocuments


class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['brand_name', 'brand_code', 'brand_activate_number', 'brand_description', 'activated_countries',
                  'brand_logo']


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = ['product_model', 'brand']


class ProductsForm(forms.ModelForm):
    class Meta:
        model = Products
        fields = [
            'prod_name',
            'prod_price',
            'currency_type',
            'prod_code',
            'quantity_type',
            'prod_desc',
            'gtip_code',
            'manufacturer_country',
            'brand',
            'prod_model',
            'manufacturer',
            'manufacturer_stock_code',
            'container_code',
            'package_lengths',
            'quantity_in_package',
            'kg',
            'kg_net',
            'package_barcode',
            'doc_name',
            'tax_code',
            'prod_img',
        ]


class UploadedDocsForm(forms.ModelForm):
    class Meta:
        model = UploadedDocuments
        fields = ["doc_type", "doc_name", "doc_file"]
