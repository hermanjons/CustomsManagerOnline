from django.db import models


# STM Bağlı İl Kodları
class Province(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "STM bağlı il kodları"
        verbose_name_plural = "STM bağlı il kodları"


# İşlem Niteliği Kodları
class TransactionType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "İşlem Niteliği Kodları"
        verbose_name_plural = "İşlem Niteliği Kodları"


# Uluslararası Liman Kodları
class Port(models.Model):
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Liman Kodları"
        verbose_name_plural = "Uluslararası Liman Kodları"


# Ödeme Şekilleri
class PaymentMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ödeme Şekilleri"
        verbose_name_plural = "Ödeme Şekilleri"


# Tamamlayıcı Bilgi Kodları
class AdditionalInfoCode(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}: {self.value}"

    class Meta:
        verbose_name = "Tamamlayıcı Bilgi Kodları"
        verbose_name_plural = "Tamamlayıcı Bilgi Kodları"


# Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları
class AntiDumpingCompany(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"
        verbose_name_plural = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"


# Gümrük İdareleri ve Saymanlık Kodları


class CustomsOffice(models.Model):
    customs_code = models.CharField(max_length=50, unique=False)
    customs_name = models.CharField(max_length=255)
    treasury_code = models.CharField(max_length=50, unique=False)
    treasury_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customs_code} - {self.customs_name} / {self.treasury_code} - {self.treasury_name}"

    class Meta:
        verbose_name = "Gümrük İdareleri ve Saymanlık Kodları"
        verbose_name_plural = "Gümrük İdareleri ve Saymanlık Kodları"


# Taşıma Araçları
class TransportVehicle(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Taşıma Araçları"
        verbose_name_plural = "Taşıma Araçları"


# Uluslararası Anlaşma Kodları
class InternationalAgreement(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Anlaşma Kodları"
        verbose_name_plural = "Uluslararası Anlaşma Kodları"


# Basitleştirilmiş Usul Kodları
class SimplifiedProcedure(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Basitleştirilmiş Usul Kodları"
        verbose_name_plural = "Basitleştirilmiş Usul Kodları"


# Liman Kodları
class Harbor(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Liman Kodları"
        verbose_name_plural = "Liman Kodları"


# Ölçü Birimleri Kodları
class MeasurementUnit(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ölçü Birimleri Kodları"
        verbose_name_plural = "Ölçü Birimleri Kodları"


# Muafiyet Kodları
class ExemptionCode(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Muafiyet Kodları"
        verbose_name_plural = "Muafiyet Kodları"


# İstenen Döküman Kodları
class RequiredDocument(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "İstenen Döküman Kodları"
        verbose_name_plural = "İstenen Döküman Kodları"


# Havalimanı Kodları
class Airport(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Havalimanı Kodları"
        verbose_name_plural = "Havalimanı Kodları"


# Uçak Şirketi Kodları
class AirlineCompany(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uçak Şirketi Kodları"
        verbose_name_plural = "Uçak Şirketi Kodları"


# Teslim Şekli Kodları
class DeliveryMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Teslim Şekli Kodları"
        verbose_name_plural = "Teslim Şekli Kodları"


# Güncel Vergi Kodları
class TaxCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Güncel Vergi Kodları"
        verbose_name_plural = "Güncel Vergi Kodları"


# Taşıma Türleri Kodları
class TransportType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Taşıma Türleri Kodları"
        verbose_name_plural = "Taşıma Türleri Kodları"


# Kap Kodları
class ContainerCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Kap Kodları"
        verbose_name_plural = "Kap Kodları"


# Döviz Cinsi Kodları
class CurrencyType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Döviz Cinsi Kodları"
        verbose_name_plural = "Döviz Cinsi Kodları"


# Ülke Kodları
class Country(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ülke Kodları"
        verbose_name_plural = "Ülke Kodları"


# Rejim Kodları
class RegimeCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Rejim Kodları"
        verbose_name_plural = "Rejim Kodları"


# Ambar Kodları
class Warehouse(models.Model):
    warehouse_code = models.CharField(max_length=10)
    warehouse_name = models.CharField(max_length=255)
    customs_name = models.CharField(max_length=255)
    customs_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.warehouse_code} - {self.warehouse_name} / {self.customs_code} - {self.customs_name}"

    class Meta:
        verbose_name = "Ambar Kodları"
        verbose_name_plural = "Ambar Kodları"


# Antrepo Kodları
class Depot(models.Model):
    depot_code = models.CharField(max_length=10, unique=True)
    depot_name = models.CharField(max_length=255)
    customs_name = models.CharField(max_length=255)
    customs_code = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.depot_code} - {self.depot_name} / {self.customs_code} - {self.customs_name}"

    class Meta:
        verbose_name = "Antrepo Kodları"
        verbose_name_plural = "Antrepo Kodları"


# Banka Kodları
class Bank(models.Model):
    swift_code = models.CharField(max_length=50)
    bank_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=40)
    fax_number = models.CharField(max_length=100)
    web_address = models.CharField(max_length=255)
    kep_address = models.CharField(max_length=100)
    eft_number = models.CharField(max_length=100)


    def __str__(self):
        return f"{self.swift_code} - {self.bank_name} / {self.address} - {self.phone_number}" \
               f"{self.fax_number} - {self.web_address} / {self.kep_address} - {self.eft_number}"


    class Meta:
        verbose_name = "Banka Kodları"
        verbose_name_plural = "Banka Kodları"


class BankBranches(models.Model):
    bank_connection = models.ForeignKey(Bank, on_delete=models.CASCADE, max_length=100)
    branches_number = models.CharField(max_length=50)
    branches_name = models.CharField(max_length=255)
    branch_acc_number = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.branches_number} - {self.branches_name} / {self.branch_acc_number} - {self.bank_connection}" \



    class Meta:
        verbose_name = "Banka şubeleri"
        verbose_name_plural = "Banka şubeleri"
