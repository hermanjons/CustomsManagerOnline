# products/urls.py - URL Yönlendirme Dokümantasyonu

Bu dosya, `products` Django uygulamasına ait URL yönlendirmelerini tanımlar. Her bir URL rotasının ne işe yaradığı ve hangi view (görünüm) ile bağlantılı olduğu aşağıda detaylı olarak verilmiştir.

## Marka (Brand) İşlemleri

* **`GET /brands/`**
  `BrandListView`

  > Marka listesini görüntüler.

* **`GET, POST /brands/create/`**
  `BrandCreateView`

  > Yeni marka ekleme formu.

## Ürün Modeli (Product Model) İşlemleri

* **`GET /models/`**
  `ProductModelListView`

  > Tüm ürün modellerinin listesi.

* **`GET, POST /models/create/`**
  `ProductModelCreateView`

  > Yeni bir ürün modeli oluşturma formu.

## Ürünler (Products)

* **`GET /products/`**
  `ProductsListView`

  > Tüm ürünleri listeler.

* **`GET, POST /products/create/`**
  `ProductsCreateView`

  > Yeni bir ürün oluşturma formu.

## Yüklenmiş Belgeler (Uploaded Documents)

* **`GET /uploadeddocs/`**
  `UploadedDocsListView`

  > Yüklenmiş belgelerin listesi.

* **`GET, POST /uploadeddocs/create/`**
  `UploadedDocsCreateView`

  > Yeni belge yükleme formu.

## AJAX Aramaları

* **`GET /ajax/tax-code-search/`**
  `TaxCodeModalSearch`

  > Vergi kodu için canlı arama.

* **`GET /ajax/gtip-code-search/`**
  `GtipCodeModalSearch`

  > GTİP kodu için canlı arama.

* **`GET /ajax/document-search/`**
  `UploadedDocsModalSearch`

  > Belgeler için modal içi arama.
