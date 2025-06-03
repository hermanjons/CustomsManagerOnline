# 👁️ `core/views.py` Açıklaması

Bu dosya, projede dinamik olarak listeleme, arama, sayfalama ve detay görüntüleme gibi işlevleri sağlayan genelleştirilmiş (generic) görünümler (views) içerir. Özellikle listeleme sayfaları benzeri yapılarda veya frontend üzerinden JSON veri ihtiyacı olan sistemlerde kullanılmak üzere hazırlanmıştır.

---

## 1. `GenericFilteredListView`

`ListView`'den türeyen bu sınıf, filtreleme, sayfalama ve dinamik field gösterimi gibi işlemleri esnek bir şekilde sağlar.

### Temel Nitelikler:

* `model`: Listelemede kullanılacak model
* `query_param`: Arama yapılacak GET parametresi (varsayılan: `'q'`)
* `search_fields`: Aranabilir alanlar (opsiyonel)
* `related_search_fields`: FK veya M2M gibi alanlarda arama yapabilmek için
* `paginate_by_default`: Sayfalama için varsayılan değer

### Override Edilen Methodlar:

* `get_search_fields()`:
  Otomatik olarak `CharField` ve `TextField` türü alanları seçer veya manuel tanımlanan alanları döner.

* `get_related_search_fields()`:
  FK veya M2M alanlar için arama yapılacak isimleri döner.

* `get_queryset()`:
  Arama parametresine göre queryset filtrelemesi yapar. `Q` objesi ile birleştirme yapar.

* `get_paginate_by()`:
  GET üzerinden gelen `per_page` değerini kontrol eder. Sayfa başı kayıt sayısını belirler.

* `get_visible_fields()`:
  Hangi alanların görüneceğine karar verir. `visible_fields` veya `excluded_fields` tanımlı olabilir.

* `get_model_meta_context()`:
  Arayüz için model adı, ikon, alan isimleri gibi bilgiler sağlar.

* `get_model_meta_json()`:
  JSON çıktı için `get_model_meta_context`'in sadeleştirilmiş versiyonudur.

* `get_object_detail_json(pk)`:
  Verilen `pk` ile model nesnesini getirir ve alan değerlerini JSON olarak döner.

* `get_context_data()`:
  Sayfa içeriğine özel veri ve meta bilgiler ekler.

---

## 2. `AjaxFilteredListView`

Bu sınıf, `GenericFilteredListView`'den türemiştir ve tek farkı, sonucun HTML yerine **JSON** olarak dönmesidir.

### Override:

* `render_to_response()`:
  `context['object_list']` üzerinden queryset'i `values()` ile JSON'a çevirir.

### Kullanım Amaçları:

* Canlı arama (autocomplete)
* Dinamik tablo veri çekimi
* SPA veya AJAX tabanlı veri istekleri

---

Bu view yapıları, projedeki çok sayıda modelin arayüzde dinamik, esnek ve uyumlu şekilde işlenebilmesini sağlamak için tasarlanmıştır.
