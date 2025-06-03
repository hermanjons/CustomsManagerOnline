from django.db import models
from customs_general.models import RequiredDocument, CurrencyType, QuantityType, GtipCode, ContainerCode, \
    TaxCode, Country
from core.models import UploadedDocumentsBase


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_code = models.CharField(max_length=100)
    brand_activate_number = models.CharField(max_length=100)
    brand_description = models.CharField(max_length=255)
    activated_countries = models.ForeignKey(Country, on_delete=models.CASCADE)
    brand_logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True, verbose_name="Marka görseli")

    custom_model = True

    def __str__(self):
        return f"{self.brand_name} - {self.brand_code} / {self.brand_activate_number}"

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Marka"


class ProductModel(models.Model):
    product_model = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    custom_model = True

    def __str__(self):
        return f"{self.product_model}"

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Model"


class UploadedDocuments(UploadedDocumentsBase):
    doc_type = models.ForeignKey(RequiredDocument, on_delete=models.CASCADE)
    custom_model = True

    def __str__(self):
        return f"{self.product_model}"

    class Meta:
        verbose_name = "Yüklenen Dökümanlar"
        verbose_name_plural = "Yüklenen Dökümanlar"


class Products(models.Model):
    prod_name = models.CharField(max_length=255)
    prod_price = models.CharField(max_length=50)
    currency_type = models.ForeignKey(CurrencyType, on_delete=models.PROTECT)
    prod_code = models.CharField(max_length=150)
    quantity_type = models.ForeignKey(QuantityType, on_delete=models.PROTECT)
    prod_desc = models.CharField(max_length=255)
    gtip_code = models.ForeignKey(GtipCode, on_delete=models.PROTECT)
    manufacturer_country = models.ForeignKey(Country, on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    prod_model = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=150)
    manufacturer_stock_code = models.CharField(max_length=100)
    container_code = models.ForeignKey(ContainerCode, on_delete=models.PROTECT)
    package_lengths = models.CharField(max_length=100)
    quantity_in_package = models.CharField(max_length=100)
    kg = models.CharField(max_length=30)
    kg_net = models.CharField(max_length=30)
    package_barcode = models.CharField(max_length=30)
    doc_name = models.ManyToManyField(UploadedDocuments, blank=True)
    tax_code = models.ManyToManyField(TaxCode, blank=True)
    prod_img = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Ürün görseli")

    class Meta:
        verbose_name = "Ürünler"
        verbose_name_plural = "Ürünler"

    def __str__(self):
        return f"{self.prod_name} - {self.brand} - {self.prod_price} - {self.quantity_in_package} - {self.prod_desc}"
