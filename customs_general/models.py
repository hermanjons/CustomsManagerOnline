from django.db import models


# Döviz Cinsi Kodları
class CurrencyType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=150)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Döviz Cinsi Kodları"
        verbose_name_plural = "Döviz Cinsi Kodları"


# Ülke Kodları
class Country(models.Model):
    country_code_alpha2 = models.CharField(max_length=100)
    country_code_alpha3 = models.CharField(max_length=100)
    country_name_tr = models.CharField(max_length=100)
    country_name_en = models.CharField(max_length=100)
    country_number = models.CharField(max_length=100)
    country_lang_code = models.CharField(max_length=100, null=True)
    country_phone_code = models.CharField(max_length=100, null=True)
    currency_id = models.ManyToManyField(CurrencyType, blank=True, null=True)

    custom_model = True

    def __str__(self):
        return f"{self.country_code_alpha2} - {self.country_code_alpha3} -" \
               f" {self.country_number} - {self.currency_id}"

    class Meta:
        verbose_name = "Ülke Kodları"
        verbose_name_plural = "Ülke Kodları"


class City(models.Model):
    code = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=255)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name} - {self.country_id}"

    class Meta:
        verbose_name = "Şehirler"
        verbose_name_plural = "Şehirler"


# İşlem Niteliği Kodları
class TransactionType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "İşlem Niteliği Kodları"
        verbose_name_plural = "İşlem Niteliği Kodları"


# Uluslararası Liman Kodları
class Port(models.Model):
    code = models.CharField(max_length=60, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    city_id = models.ForeignKey(City,on_delete=models.CASCADE, null=True)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Liman Kodları"
        verbose_name_plural = "Uluslararası Liman Kodları"


# Ödeme Şekilleri
class PaymentMethod(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    risk_status = models.CharField(max_length=100)
    usage_status = models.CharField(max_length=100)
    edi_code = models.CharField(max_length=100)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name} / {self.edi_code}"

    class Meta:
        verbose_name = "Ödeme Şekilleri"
        verbose_name_plural = "Ödeme Şekilleri"


class PaymentType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    risk_status = models.CharField(max_length=100)
    usage_status = models.CharField(max_length=100)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ödeme Tipleri"
        verbose_name_plural = "Ödeme Tipleri"


# Tamamlayıcı Bilgi Kodları
class AdditionalInfoCode(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.description}: {self.value}"

    class Meta:
        verbose_name = "Tamamlayıcı Bilgi Kodları"
        verbose_name_plural = "Tamamlayıcı Bilgi Kodları"


# Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları
class AntiDumpingCompany(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"
        verbose_name_plural = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"


# gümrük tipleri
class CustomsType(models.Model):
    code = models.CharField(max_length=50, unique=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Gümrük tipleri"
        verbose_name_plural = "Gümrük tipleri"


class ChiefCustomsOffice(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Başgümrük Müdürlükleri"
        verbose_name_plural = "Başgümrük Müdürlükleri"


# Gümrük İdareleri

class CustomsOffice(models.Model):
    name = models.CharField(max_length=100, unique=False)
    code = models.CharField(max_length=255)
    customs_type_id = models.ManyToManyField(CustomsType, null=True, blank=True)
    chief_customs_id = models.ForeignKey(ChiefCustomsOffice, on_delete=models.CASCADE, null=True, blank=True)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    custom_model = True

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Gümrük İdareleri ve Saymanlık Kodları"
        verbose_name_plural = "Gümrük İdareleri ve Saymanlık Kodları"


# Taşıma Araçları
class TransportVehicle(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Taşıma Araçları"
        verbose_name_plural = "Taşıma Araçları"


# Uluslararası Anlaşma Kodları
class InternationalAgreement(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Anlaşma Kodları"
        verbose_name_plural = "Uluslararası Anlaşma Kodları"


# Basitleştirilmiş Usul Kodları
class SimplifiedProcedure(models.Model):
    code = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Basitleştirilmiş Usul Kodları"
        verbose_name_plural = "Basitleştirilmiş Usul Kodları"


# Liman Kodları
class Harbor(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Liman Kodları"
        verbose_name_plural = "Liman Kodları"


# Muafiyet Kodları
class ExemptionCode(models.Model):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Muafiyet Kodları"
        verbose_name_plural = "Muafiyet Kodları"


# belge kodları
class RequiredDocument(models.Model):
    code = models.CharField(max_length=70)
    name = models.CharField(max_length=255)
    edi_code = models.CharField(max_length=150)
    name_en = models.CharField(max_length=150)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "İstenen Döküman Kodları"
        verbose_name_plural = "İstenen Döküman Kodları"


# Havalimanı Kodları
class Airport(models.Model):
    code_iata = models.CharField(max_length=10, unique=True, blank=True, null=True)
    code_icao = models.CharField(max_length=255, unique=True, blank=True, null=True)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    latitude_degree = models.CharField(max_length=80, blank=True, null=True)
    longitude_degree = models.CharField(max_length=100, blank=True, null=True)

    custom_model = True

    def __str__(self):
        return f"{self.code_iata} - {self.code_icao} - {self.city_id}"

    class Meta:
        verbose_name = "Havalimanı Kodları"
        verbose_name_plural = "Havalimanı Kodları"


# Uçak Şirketi Kodları
class AirlineCompany(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uçak Şirketi Kodları"
        verbose_name_plural = "Uçak Şirketi Kodları"


# Teslim Şekli Kodları
class DeliveryMethod(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=200)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Teslim Şekli Kodları"
        verbose_name_plural = "Teslim Şekli Kodları"


# Güncel Vergi Kodları
class TaxCode(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    tax_ratio = models.IntegerField(null=True)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Güncel Vergi Kodları"
        verbose_name_plural = "Güncel Vergi Kodları"


# Taşıma Türleri Kodları
class TransportType(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name_tr = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True)

    edi_code = models.IntegerField(null=True)
    e_invoice_code = models.IntegerField(null=True)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name_tr}/{self.edi_code} - {self.e_invoice_code}"

    class Meta:
        verbose_name = "Taşıma Türleri Kodları"
        verbose_name_plural = "Taşıma Türleri Kodları"


# Kap Kodları
class ContainerCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Kap Kodları"
        verbose_name_plural = "Kap Kodları"


# Rejim Kodları
class RegimeCode(models.Model):
    code = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "Rejim Kodları"
        verbose_name_plural = "Rejim Kodları"


# Ambar Kodları
class Warehouse(models.Model):
    warehouse_code = models.CharField(max_length=10)
    warehouse_name = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.warehouse_code} - {self.warehouse_name}"

    class Meta:
        verbose_name = "Ambar Kodları"
        verbose_name_plural = "Ambar Kodları"


# Antrepo Kodları
class Depot(models.Model):
    depot_code = models.CharField(max_length=60)
    depot_name = models.CharField(max_length=255)
    customs_number = models.ForeignKey(CustomsOffice, on_delete=models.CASCADE)
    warehouse_code = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    custom_model = True

    def __str__(self):
        return f"{self.depot_code} - {self.depot_name} / {self.customs_number} - {self.warehouse_code}"

    class Meta:
        verbose_name = "Antrepo Kodları"
        verbose_name_plural = "Antrepo Kodları"


# Banka Kodları
class Bank(models.Model):
    swift_code = models.CharField(max_length=50, null=True)
    bank_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    eft_number = models.IntegerField(null=True)
    bank_logo = models.ImageField(upload_to="customs_general/", blank=True, null=True, verbose_name="Ürün görseli")
    custom_model = True

    def __str__(self):
        return f"{self.swift_code} - {self.bank_name} / {self.address}"

    class Meta:
        verbose_name = "Banka Kodları"
        verbose_name_plural = "Banka Kodları"


# Bank sınıfıyla ilişkili sınıf
class BankBranches(models.Model):
    bank_id = models.ForeignKey(Bank, on_delete=models.CASCADE, max_length=100)
    branches_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    city_id = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    custom_model = True

    def __str__(self):
        return f"{self.branches_code} - {self.name}"

    class Meta:
        verbose_name = "Banka şubeleri"
        verbose_name_plural = "Banka şubeleri"


class QuantityType(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    edi_code = models.CharField(max_length=10)
    custom_model = True

    def __str__(self):
        return f"{self.name} - {self.code} / {self.name_en} - {self.edi_code}"

    class Meta:
        verbose_name = "Miktar Cinsleri"
        verbose_name_plural = "Miktar cinsleri"


class CustomerType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=255)
    custom_model = True

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Müşteri tipleri"
        verbose_name_plural = "Müşteri tipleri"


class GtipCode(models.Model):
    code = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    quantity = models.CharField(max_length=50)
    tax_code = models.ForeignKey(TaxCode, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.code} - {self.desc} - {self.quantity} - {self.tax_code}"

    class Meta:
        verbose_name = "GTİP Kodları"
        verbose_name_plural = "GTİP Kodları"
