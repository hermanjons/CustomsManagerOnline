# customs\_general/models.py Belgelendirme

Bu dosya, gümrükleme işlemleriyle ilgili sabit tanımlamaları içeren modelleri tanımlar. Modeller, genellikle idari alanlarda kullanıma yönelik olarak ülke, şehir, liman, döviz, ödeme, vergi gibi tanımlamalardan oluşur. Tüm modeller `AuditModel` ya da türevlerinden miras alarak denetim ve izleme altyapısı sağlar.

## Soyut Model Türevleri

* **AuditModel**: Oluşturulma ve güncellenme bilgilerini tutar.
* **AuditModelWithSource**: Ek olarak verinin geldiği veri kaynağını (`data_source`) içerir.
* **AuditModelWithId**: ID alanı elle belirlenen modeller için kullanılır.
* **AuditModelWithIdAndSource**: Hem ID hem kaynak bilgisi içerir.

## Modellerin Tanımı

Aşağıda her bir modelin neyi temsil ettiği kısaca açıklanmıştır:

* **DataSource**: Verinin kaynağını temsil eder (manuel, excel, api, vb.).
* **CurrencyType**: Para birimi bilgileri (USD, EUR, vb.).
* **Country**: Ülkeler ve onlara ait kodlar, telefon kodu, dil, vb.
* **City**: Şehir bilgileri. Ülkeye bağlıdır, kendine referansla şehir hiyerarşisi kurulabilir.
* **TransactionType**: Gümrük işlem niteliği kodları.
* **Port**: Uluslararası liman bilgileri.
* **PaymentMethod**: Ödeme şekilleri (ör. peşin, akreditif).
* **PaymentType**: Ödeme tipleri (ör. mal bedeli, navlun).
* **AdditionalInfoCode**: Tamamlayıcı bilgi kodları.
* **AntiDumpingCompany**: Anti-damping kapsamında üretici/gönderici firma bilgisi.
* **CustomsType**: Gümrük türleri.
* **ChiefCustomsOffice**: Başgümrük müdürlükleri.
* **CustomsOffice**: Gümrük idareleri. Gümrük türleriyle ve baş müdürlükle ilişkilidir.
* **TransportVehicle**: Taşıma araçları (kamyon, uçak, gemi, vb.).
* **InternationalAgreement**: Uluslararası anlaşmalar.
* **SimplifiedProcedure**: Basitleştirilmiş usuller.
* **ExemptionCode**: Muafiyet kodları.
* **RequiredDocument**: Talep edilen belgeler (ör. ATR, fatura).
* **Airport**: Havalimanları (IATA ve ICAO kodları).
* **AirlineCompany**: Havayolu şirketleri.
* **DeliveryMethod**: Teslim şekli tanımları (FOB, CIF, vb.).
* **TaxCode**: Vergi türleri ve kodları.
* **TransportType**: Taşıma türleri (kara, hava, deniz, vb.).
* **ContainerCode**: Konteyner türleri (20FT, 40FT, vb.).
* **RegimeCode**: Rejim kodları (ör. serbest dolaşım).
* **Warehouse**: Ambar tanımları.
* **Depot**: Antrepo tanımları. Ambar ve gümrük idaresiyle bağlantılıdır.
* **Bank**: Banka bilgileri, şube kodları, logo, vb.
* **BankBranches**: Banka şubeleri.
* **QuantityType**: Miktar türleri (kg, adet, litre, vb.).
* **CustomerType**: Müşteri türleri (gerçek kişi, tüzel kişi).
* **GtipCode**: GTİP (Gümrük Tarife İstatistik Pozisyonu) kodları.

## Ek Notlar

* Modeller `__str__` metodu ile okunabilir şekilde tanımlanmıştır.
* Gelişmiş temizleme (validation) `DataSource.clean()` metodunda örneklenmiştir.
* ForeignKey ve ManyToManyField kullanımı ile veri bütünlüğü ve ilişkilendirme sağlanmıştır.

Bu modeller, dış ticaret ve gümrük işlemleriyle ilgili her türlü tanım verisinin sistemde yönetilebilmesini sağlar.
