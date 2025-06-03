# products/views.py - Görünümler (Views) Dokümantasyonu

Bu doküman, `products/views.py` dosyasında tanımlı sınıfların (views) ne işe yaradığını açıklar. Her bir view, belirli bir modeli ve formu kullanarak web arayüzü ile etkileşim sağlar.

## Marka (Brand) View'ları

### BrandCreateView

* **Tür**: `CreateView`
* **Model**: `Brand`
* **Form**: `BrandForm`
* **Template**: `products/brand_create.html`
* **Açıklama**: Yeni bir marka oluşturmak için kullanılır.

### BrandListView

* **Tür**: `GenericFilteredListView`
* **Model**: `Brand`
* **Template**: `products/brand_page.html`
* **Açıklama**: Marka listesini filtrelenebilir olarak sunar.

## Ürün Modeli (Product Model) View'ları

### ProductModelCreateView

* **Tür**: `CreateView`
* **Model**: `ProductModel`
* **Form**: `ProductModelForm`
* **Template**: `products/model_create.html`

### ProductModelListView

* **Tür**: `GenericFilteredListView`
* **Model**: `ProductModel`
* **Template**: `products/model_page.html`
* **related\_search\_fields**: `brand__brand_name`
* **Açıklama**: Ürün modellerini listeler ve tüm arama alanlarına ek olarak ilişkili marka ismine göre filtreleme yapar.

## Ürünler (Products) View'ları

### ProductsListView

* **Tür**: `GenericFilteredListView`
* **Model**: `Products`
* **Template**: `products/products_page.html`
* **related\_search\_fields**: `brand__brand_name`

### ProductsCreateView

* **Tür**: `CreateView`
* **Model**: `Products`
* **Form**: `ProductsForm`
* **Template**: `products/products_create.html`
* **Açıklama**: Ürün oluşturur ve `tax_code`, `doc_name` alanlarını ManyToMany şekilde post verisi ile ayarlar.

## Belgeler (UploadedDocuments) View'ları

### UploadedDocsListView

* **Tür**: `GenericFilteredListView`
* **Model**: `UploadedDocuments`
* **Template**: `products/uploaded_docs_page.html`

### UploadedDocsCreateView

* **Tür**: `CreateView`
* **Model**: `UploadedDocuments`
* **Form**: `UploadedDocsForm`
* **Template**: `products/uploaded_docs_create.html`

## AJAX Arama View'ları

### UploadedDocsModalSearch

* **Tür**: `AjaxFilteredListView`
* **Model**: `UploadedDocuments`
* **search\_fields**: `doc_name`

### TaxCodeModalSearch

* **Tür**: `AjaxFilteredListView`
* **Model**: `TaxCode`

### GtipCodeModalSearch

* **Tür**: `AjaxFilteredListView`
* **Model**: `GtipCode`
