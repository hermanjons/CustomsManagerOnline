# `products/forms.py` Açıklaması

Bu dosya, `products` uygulamasındaki modeller için Django `ModelForm` sınıflarını içerir. Amaç, kullanıcıdan alınan verilerin hem doğrulamasını yapmak hem de bu verileri doğrudan ilgili modelle eşleştirerek veritabanına güvenli şekilde kaydedebilmektir.

---

## 1. `BrandForm`

* `Brand` modeline bağlı bir formdur.
* Aşağıdaki alanları içerir:

  * `brand_name`, `brand_code`, `brand_activate_number`, `brand_description`, `activated_countries`, `brand_logo`
* Bu form, marka bilgilerini kullanıcıdan toplamak için kullanılır.

---

## 2. `ProductModelForm`

* `ProductModel` modeline bağlıdır.
* Alanlar:

  * `product_model`, `brand`
* Belirli bir markaya ait ürün modelini tanımlamak için kullanılır.

---

## 3. `ProductsForm`

* `Products` modeline bağlı, en kapsamlı form yapısıdır.
* Çok sayıda ürün alanını içerir:

  * Ürün adı, fiyatı, döviz cinsi, GTIP kodu, üretici, marka, model, paketleme, vergi kodu, ürün görseli vb.
* Kullanıcıdan detaylı ürün verisi almak ve doğrudan modele kaydetmek için kullanılır.

---

## 4. `UploadedDocsForm`

* `UploadedDocuments` modeline bağlı formdur.
* Alanlar:

  * `doc_type`, `doc_name`, `doc_file`
* Doküman yükleme işlemleri için kullanılır (örn. ürün belgeleri).

---

## Teknik Not

Bu formlar `forms.ModelForm` sınıfından türetilmiştir. Django’da `ModelForm`, formun hangi modele ait olduğunu ve hangi alanları içereceğini `Meta` iç içe sınıfı üzerinden öğrenir. Bu yapı sayesinde:

* Otomatik form alanları üretilir
* Modelde tanımlı validasyon kuralları (örneğin `blank=False`) formda da geçerli olur
* `.save()` metodu ile model nesnesi doğrudan veritabanına kaydedilebilir

Bu yapı, hem güvenli hem de minimum kod ile form işlemlerinin gerçekleştirilmesini sağlar.
