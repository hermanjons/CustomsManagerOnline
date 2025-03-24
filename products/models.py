from django.db import models
from customs_general.models import Country


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)
    brand_code = models.CharField(max_length=100)
    brand_activate_number = models.CharField(max_length=100)
    brand_description = models.CharField(max_length=255)
    activated_countries = models.ForeignKey(Country, on_delete=models.CASCADE)
    brand_logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True, verbose_name="Marka görseli")