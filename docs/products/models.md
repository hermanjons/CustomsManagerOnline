# `products/models.py` Açıklaması

Bu dosya, `products` uygulamasına ait ürün, marka, model ve yüklenen belgelerle ilgili veri yapılarının tanımlandığı yerdir. Her model, gerçek dünyadaki bir kavramı temsil eder ve Django ORM aracılığıyla veritabanı işlemlerine olanak sağlar.

---

## 1. `Brand`

Marka bilgisini temsil eden modeldir.

**Alanlar:**

* `brand_name`, `brand_code`, `brand_activate_number`, `brand_description`: Metinsel tanımlayıcı bilgiler.
* `activated_countries`: Hangi ülkelerde aktif olduğu.
* `brand_logo`: Marka logosu görseli (opsiyonel).

**Özellikler:**

* `__str__`: Marka adı, kodu ve aktivasyon numarasını birleştirerek gösterir.
* `custom_model`: Sisteme, özel tanım olduğunu belirten bayrak.

---

## 2. `ProductModel`

Bir markaya bağlı ürün modeli bilgisini tutar.

**Alanlar:**

* `product_model`: Model adı.
* `brand`: İlişkili olduğu marka.

**Özellikler:**

* `__str__`: Sadece model adını gösterir.
* `custom_model`: Sisteme özel olduğunu belirtir.

---

## 3. `UploadedDocuments`

Yüklenen dokümanları temsil eder (örn. teknik döküman, sertifika vb).

**Alanlar:**

* `doc_type`: Belge tipi (`RequiredDocument` modeli ile ilişkili).
* `doc_name`: Belge adı.
* `doc_file`: Dosyanın kendisi. `date_based_upload_path` fonksiyonu sayesinde tarih bazlı klasöre kaydedilir.

**Özellikler:**

* `__str__`: Belge adı ve tipi birleştirilerek gösterilir.

---

## 4. `Products`

Ürüne ait tüm detayların tutulduğu ana modeldir.

**Temel Alanlar:**

* `prod_name`, `prod_price`, `prod_code`, `prod_desc`, `manufacturer`, `manufacturer_stock_code`, `package_lengths`, `quantity_in_package`, `kg`, `kg_net`, `package_barcode`

**İlişkisel Alanlar:**

* `currency_type`: Para birimi.
* `quantity_type`: Miktar tipi.
* `gtip_code`: GTİP kodu.
* `manufacturer_country`: Üretici ülke.
* `brand`, `prod_model`: Marka ve model.
* `container_code`: Ambalaj kodu.
* `doc_name`: İlişkili belgeler&#x20;
* `tax_code`: İlişkili vergi kodları&#x20;

**Görsel Alan:**

* `prod_img`: Ürün görseli (opsiyonel).

**Özellikler:**

* `__str__`: Ürün bilgilerini tek satırda özetleyen gösterim.
* `verbose_name`: Admin panelinde "Ürünler" olarak görünmesi sağlanır.

---

Bu modeller, ürün yönetimi ve belge takibi açısından uygulamanın temel veri yapısını oluşturur. Her biri Django’nun ORM sistemiyle doğrudan veritabanıyla eşleştirilerek CRUD işlemlerine uygun hale getirilmiştir.
