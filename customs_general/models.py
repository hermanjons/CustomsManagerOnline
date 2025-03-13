from django.db import models


# STM Bağlı İl Kodları
class Province(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


# İşlem Niteliği Kodları
class TransactionType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Uluslararası Liman Kodları
class Port(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name} ({self.country})"


# Ödeme Şekilleri
class PaymentMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Tamamlayıcı Bilgi Kodları
class AdditionalInfoCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}: {self.value}"


# Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları
class AntiDumpingCompany(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Gümrük İdareleri ve Saymanlık Kodları
class CustomsOffice(models.Model):
    customs_code = models.CharField(max_length=50, unique=False)
    customs_name = models.CharField(max_length=255)
    treasury_code = models.CharField(max_length=50, unique=False)
    treasury_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customs_code} - {self.customs_name} / {self.treasury_code} - {self.treasury_name}"


# Taşıma Araçları
class TransportVehicle(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Uluslararası Anlaşma Kodları
class InternationalAgreement(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Basitleştirilmiş Usul Kodları
class SimplifiedProcedure(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Liman Kodları
class Harbor(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Ölçü Birimleri Kodları
class MeasurementUnit(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Muafiyet Kodları
class ExemptionCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# İstenen Döküman Kodları
class RequiredDocument(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Havalimanı Kodları
class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Uçak Şirketi Kodları
class AirlineCompany(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Teslim Şekli Kodları
class DeliveryMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Güncel Vergi Kodları
class TaxCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Taşıma Türleri Kodları
class TransportType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Kap Kodları
class ContainerCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Döviz Cinsi Kodları
class CurrencyType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Ülke Kodları
class Country(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


# Rejim Kodları
class RegimeCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"


# Ambar Kodları
class Warehouse(models.Model):
    warehouse_code = models.CharField(max_length=10, unique=True)
    warehouse_name = models.CharField(max_length=255)
    customs_name = models.CharField(max_length=255)
    customs_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.warehouse_code} - {self.warehouse_name} / {self.customs_code} - {self.customs_name}"


# Antrepo Kodları
class Depot(models.Model):
    depot_code = models.CharField(max_length=10, unique=True)
    depot_name = models.CharField(max_length=255)
    customs_name = models.CharField(max_length=255)
    customs_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.depot_code} - {self.depot_name} / {self.customs_code} - {self.customs_name}"


# Banka Kodları
class Bank(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"
