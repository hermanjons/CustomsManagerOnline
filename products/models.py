from django.db import models
from customs_general.models import Country


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_code = models.CharField(max_length=100)
    brand_activate_number = models.CharField(max_length=100)
    brand_description = models.CharField(max_length=255)
    activated_countries = models.ForeignKey(Country, on_delete=models.CASCADE)
    brand_logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True, verbose_name="Marka görseli")

    custom_model = True

    def __str__(self):
        return f"{self.brand_name} - {self.brand_code} / {self.brand_activate_number} - {self.brand_description}" \
               f"{self.activated_countries} - {self.brand_logo}"

    class Meta:
        verbose_name = "Marka"
        verbose_name_plural = "Marka"


class ProductModel(models.Model):
    product_model = models.CharField(max_length=100)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    custom_model = True

    def __str__(self):
        return f"{self.product_model} - {self.brand}"

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Model"
