# 📂 `core/models.py` Açıklaması

Bu dosya, projede sık kullanılan **soyut (abstract) model yapılarını** tanımlar. Ortak alanları tekrar tekrar tanımlamamak için kalıp görevindedir. Tüm uygulamalar bu modelleri miras alarak kullanabilir.

---

## 1. `TimeStampedModel`

* Otomatik olarak oluşma ve güncellenme zamanını tutar.
* Alanlar:

  * `created_at` — Nesne ilk oluştuğunda otomatik atanır.
  * `updated_at` — Nesne her kaydedildiğinde otomatik güncellenir.
* Soyut bir modeldir.

---

## 2. `SoftDeleteModel`

* Silme yerine pasifleştirme için kullanılır.
* Alan:

  * `is_active` — Kaydın aktif olup olmadığını belirtir.
* Gerçek silme yerine filtreleme ile pasif kayıtlar gizlenebilir.

---

## 3. `AuditModel`

* Hem `TimeStampedModel` hem `SoftDeleteModel` özelliklerini birleştirir.
* Ekstra olarak:

  * `custom_model = True` — Sisteme ait özel tanımlı model işareti.
* Alt sınıflarda kullanılmak üzere soyut bir temel modeldir.

---

## 4. `AuditModelWithId`

* `AuditModel` tabanlı modeldir.
* Alan:

  * `id` — Primary key olarak elle verilecek integer ID.
* Otomatik artan ID yerine dışarıdan ID verilecek durumlar için kullanılır.

---

## 5. `AuditModelWithSource`

* `AuditModel` tabanlı modeldir.
* Alan:

  * `data_source` — Kaynağı temsil eden FK, nullable.
  * Gümrük veri setlerinde verinin kaynağını takip etmek için kullanılır.

---

## 6. `AuditModelWithIdAndSource`

* Hem `AuditModelWithId` hem `AuditModelWithSource` özelliklerini birleştirir.
* Hem ID'yi manuel vermek hem de veri kaynağını belirtmek gerekiyorsa kullanılır.

---

Bu yapılar, tüm modellerde tekrarlanan alanları merkezi bir yerde tutarak **bakım kolaylığı**, **standartlaşma** ve **temiz kod** sağlar.
