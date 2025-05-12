from django.db import models
from core.models import AuditModel, AuditModelWithSource, AuditModelWithId, AuditModelWithIdAndSource
from django.core.exceptions import ValidationError


class DataSource(AuditModelWithId):
    name = models.CharField(max_length=255, unique=True)
    source_type = models.CharField(max_length=50, choices=[
        ("manual", "Manuel Giriş"),
        ("import_excel", "Excel Yükleme"),
        ("api", "API Üzerinden"),
        ("integration", "Harici Entegrasyon"),
        ("other", "Diğer"),
    ])
    description = models.TextField(blank=True, null=True)
    is_global = models.BooleanField(default=False, verbose_name="Uluslararası Kayıt")
    origin_country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Kaynak Ülke"
    )

    def clean(self):
        if self.is_global and self.origin_country is not None:
            raise ValidationError("Uluslararası kayıtlar için ülke seçilmemelidir.")
        if not self.is_global and self.origin_country is None:
            raise ValidationError("Yerel kayıtlar için ülke seçilmelidir.")

    def __str__(self):
        return f"{self.name} ({self.get_source_type_display()})"

    class Meta:
        verbose_name = "Veri Kaynağı"
        verbose_name_plural = "Veri Kaynakları"


# Döviz Cinsi Kodları
class CurrencyType(AuditModelWithIdAndSource):
    currency_code_3_alpha = models.CharField(max_length=30)
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=150)
    name_tr = models.CharField(max_length=150)
    minor_unit = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Döviz Cinsi Kodları"
        verbose_name_plural = "Döviz Cinsi Kodları"


# Ülke Kodları
class Country(AuditModelWithSource):
    country_code_alpha2 = models.CharField(max_length=100)
    country_code_alpha3 = models.CharField(max_length=100)
    country_name_tr = models.CharField(max_length=100)
    country_name_en = models.CharField(max_length=100)
    country_number = models.CharField(max_length=100)
    country_lang_code = models.CharField(max_length=100, null=True)
    country_phone_code = models.CharField(max_length=100, null=True)
    currency = models.ManyToManyField(CurrencyType, blank=True, null=True)

    def __str__(self):
        return f"{self.country_code_alpha2} - {self.country_code_alpha3} -" \
               f" {self.country_number}"

    class Meta:
        verbose_name = "Ülke Kodları"
        verbose_name_plural = "Ülke Kodları"


class City(AuditModelWithIdAndSource):
    code = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=255, null=True)
    name_alternate = models.TextField(null=True, blank=True)

    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)

    # Self relation - üst şehir (örnek: Bağcılar → İstanbul)
    up_city = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="alt_yerlesimler"
    )

    # Self relation - başkent (örnek: tüm Türkiye şehirleri → Ankara)
    capitol_city = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="baskent_altindakiler"
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Şehir"
        verbose_name_plural = "Şehirler"


# İşlem Niteliği Kodları
class TransactionType(AuditModelWithIdAndSource):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}"

    class Meta:
        verbose_name = "İşlem Niteliği Kodları"
        verbose_name_plural = "İşlem Niteliği Kodları"


# Uluslararası Liman Kodları
class Port(AuditModelWithIdAndSource):
    code = models.CharField(max_length=60, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Liman Kodları"
        verbose_name_plural = "Uluslararası Liman Kodları"


# Ödeme Şekilleri
class PaymentMethod(AuditModelWithIdAndSource):
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=200, null=True, blank=True)

    standard_reference = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='localized_variants',
        verbose_name='Muadil Referans'
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ödeme Şekli"
        verbose_name_plural = "Ödeme Şekilleri"


class PaymentType(AuditModelWithIdAndSource):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Ödeme Tipleri"
        verbose_name_plural = "Ödeme Tipleri"


# Tamamlayıcı Bilgi Kodları
class AdditionalInfoCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.description}: {self.value}"

    class Meta:
        verbose_name = "Tamamlayıcı Bilgi Kodları"
        verbose_name_plural = "Tamamlayıcı Bilgi Kodları"


# Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları
class AntiDumpingCompany(AuditModelWithIdAndSource):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"
        verbose_name_plural = "Anti-Damping Vergisi Üreticisi Gönderici Firma Kodları"


# gümrük tipleri
class CustomsType(AuditModelWithIdAndSource):
    code = models.CharField(max_length=50, unique=False)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Gümrük tipleri"
        verbose_name_plural = "Gümrük tipleri"


class ChiefCustomsOffice(AuditModelWithIdAndSource):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Başgümrük Müdürlükleri"
        verbose_name_plural = "Başgümrük Müdürlükleri"


# Gümrük İdareleri

class CustomsOffice(AuditModelWithIdAndSource):
    name = models.CharField(max_length=100, unique=False)
    code = models.CharField(max_length=255)
    customs_type = models.ManyToManyField(CustomsType, null=True, blank=True)
    chief_customs = models.ForeignKey(ChiefCustomsOffice, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Gümrük İdareleri ve Saymanlık Kodları"
        verbose_name_plural = "Gümrük İdareleri ve Saymanlık Kodları"


# Taşıma Araçları
class TransportVehicle(AuditModelWithIdAndSource):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    description = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Taşıma Araçları"
        verbose_name_plural = "Taşıma Araçları"


# Uluslararası Anlaşma Kodları
class InternationalAgreement(AuditModelWithIdAndSource):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uluslararası Anlaşma Kodları"
        verbose_name_plural = "Uluslararası Anlaşma Kodları"


# Basitleştirilmiş Usul Kodları
class SimplifiedProcedure(AuditModelWithIdAndSource):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Basitleştirilmiş Usul Kodları"
        verbose_name_plural = "Basitleştirilmiş Usul Kodları"


# Muafiyet Kodları
class ExemptionCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=255)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Muafiyet Kodları"
        verbose_name_plural = "Muafiyet Kodları"


# belge kodları
class RequiredDocument(AuditModelWithIdAndSource):
    code = models.CharField(max_length=70)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=150, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "İstenen Döküman Kodları"
        verbose_name_plural = "İstenen Döküman Kodları"


# Havalimanı Kodları
class Airport(AuditModelWithIdAndSource):
    code_iata = models.CharField(max_length=10, unique=True, blank=True, null=True)
    code_icao = models.CharField(max_length=255, unique=True, blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    latitude_degree = models.CharField(max_length=80, blank=True, null=True)
    longitude_degree = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.code_iata} - {self.code_icao} - {self.city_id}"

    class Meta:
        verbose_name = "Havalimanı Kodları"
        verbose_name_plural = "Havalimanı Kodları"


# Uçak Şirketi Kodları
class AirlineCompany(AuditModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Uçak Şirketi Kodları"
        verbose_name_plural = "Uçak Şirketi Kodları"


# Teslim Şekli Kodları
class DeliveryMethod(AuditModelWithIdAndSource):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Teslim Şekli Kodları"
        verbose_name_plural = "Teslim Şekli Kodları"


# Güncel Vergi Kodları
class TaxCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=255)


    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Güncel Vergi Kodları"
        verbose_name_plural = "Güncel Vergi Kodları"


# Taşıma Türleri Kodları
class TransportType(AuditModelWithIdAndSource):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, null=True)
    transport_type = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="tasima_turleri"
    )

    def __str__(self):
        return f"{self.code} - {self.name_en}"

    class Meta:
        verbose_name = "Taşıma Türleri Kodları"
        verbose_name_plural = "Taşıma Türleri Kodları"


# Kap Kodları
class ContainerCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Kap Kodları"
        verbose_name_plural = "Kap Kodları"


# Rejim Kodları
class RegimeCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Rejim Kodları"
        verbose_name_plural = "Rejim Kodları"


# Ambar Kodları
class Warehouse(AuditModel):
    warehouse_code = models.CharField(max_length=10)
    warehouse_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.warehouse_code} - {self.warehouse_name}"

    class Meta:
        verbose_name = "Ambar Kodları"
        verbose_name_plural = "Ambar Kodları"


# Antrepo Kodları
class Depot(AuditModel):
    depot_code = models.CharField(max_length=60)
    depot_name = models.CharField(max_length=255)
    customs_number = models.ForeignKey(CustomsOffice, on_delete=models.CASCADE)
    warehouse_code = models.ForeignKey(Warehouse, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.depot_code} - {self.depot_name} / {self.customs_number} - {self.warehouse_code}"

    class Meta:
        verbose_name = "Antrepo Kodları"
        verbose_name_plural = "Antrepo Kodları"


# Banka Kodları
class Bank(AuditModel):
    swift_code = models.CharField(max_length=50, null=True)
    bank_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True)
    eft_number = models.IntegerField(null=True)
    bank_logo = models.ImageField(upload_to="customs_general/", blank=True, null=True, verbose_name="Ürün görseli")

    def __str__(self):
        return f"{self.swift_code} - {self.bank_name} / {self.address}"

    class Meta:
        verbose_name = "Banka Kodları"
        verbose_name_plural = "Banka Kodları"


# Bank sınıfıyla ilişkili sınıf
class BankBranches(AuditModelWithIdAndSource):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, max_length=100)
    branches_code = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.branches_code} - {self.name}"

    class Meta:
        verbose_name = "Banka şubeleri"
        verbose_name_plural = "Banka şubeleri"


class QuantityType(AuditModelWithIdAndSource):
    name = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    unit_symbol = models.CharField(max_length=50, null=True)


    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Miktar Cinsleri"
        verbose_name_plural = "Miktar cinsleri"


class CustomerType(AuditModelWithIdAndSource):
    name = models.CharField(max_length=50, unique=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.code}"

    class Meta:
        verbose_name = "Müşteri tipleri"
        verbose_name_plural = "Müşteri tipleri"


class GtipCode(AuditModelWithIdAndSource):
    code = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True)

    def __str__(self):
        return f"{self.code} - {self.desc}"

    class Meta:
        verbose_name = "GTİP Kodları"
        verbose_name_plural = "GTİP Kodları"
