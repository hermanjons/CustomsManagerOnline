# customs\_general/admin.py

Bu belge, `customs_general` uygulamasındaki `admin.py` dosyasının işlevlerini ve yapısını açıklar.

## Amaç

Bu dosyada tüm `customs_general` modelleri için:

* Ortak bir `CustomAdmin` sınıfı tanımlanır
* Autocomplete ve arama alanları gibi admin kolaylıkları otomatikleştirilir
* Admin arayüzüne özel bir “Excel ile Yükle” butonu eklenir
* Belirli modeller için form davranışı dinamik olarak değiştirilir

## CustomAdmin Sınıfı

### change\_list\_template

```python
change_list_template = "admin/excel_upload.html"
```

Varsayılan liste görünümü değiştirilmiş ve özel bir şablon atanmıştır. Bu şablon Excel ile veri yükleme işlemini destekleyen bir buton içerir.
Dosya yolunda gözükmese de `"templates/"` klasörünün altındaki admin klasöründen söz edilmektedir.
### get\_search\_fields

```python
def get_search_fields(self, request):
```

Modeldeki tüm `CharField` ve `TextField` alanlar `search_fields` listesine eklenir.Burada `get_search_fields` methodu override edilmiştir.
`get_search_fields` methodu normal şartlarda `ModelAdmin` sınıfının bir methodudur ve işi `ModelAdmin` içerisinde tanımlı olan `search_fields`
alanını döndürmektir.`ModelAdmin` içerisinde `search_fields` direkt olarak kullanılmak yerine bu modelle döndürülüyor ve kodlar içerisinde bu
şekilde kullanılıyordu.yani kodlar içerisinde `search_fields` attribute değerine direkt erişmek yerine bu method kullanılmıştır.
Sonuç olarak biz bu methodu override ederek programın akışına hiç bir zarar vermeden `search_fields` kullanmayı keserek,istediğimiz değerleri
vermiş oluyoruz.

### get\_autocomplete\_fields

```python
def get_autocomplete_fields(self, request):
```

`ForeignKey` ve `ManyToManyField` türündeki tüm alanlar `autocomplete` listesine eklenir.Bu method `ModelAdmin` sınıfından override edilmiştir.
`ModelAdmin` sınıfındaki aynı isimdeki method işlev olarak `autocomplete_fields` attribute değerini döndürmektedir.
### get\_raw\_id\_fields

```python
def get_raw_id_fields(self, request):
    return []
```

Varsayılan olarak boş bir liste döner. Gerekirse genişletilebilir.

### get\_form

```python
def get_form(self, request, obj=None, **kwargs):
```

Sadece `PaymentMethod` modeli için geçerli özel bir durum uygulanır. Eğer bağlı olduğu `data_source` global olarak işaretlenmişse, `standard_reference` alanı formdan kaldırılır.
Bu method yine `ModelAdmin` sınıfından override edilmiştir
### changelist\_view

```python
def changelist_view(self, request, extra_context=None):
```

Liste görünümüne, modele özel olarak oluşturulmuş bir "Excel ile Yükle" butonu eklenir. Ek bağlam ile şablona gerekli bilgiler gönderilir.

### get\_urls

```python
def get_urls(self):
```

Varsayılan admin URL’lerine ek olarak her model için upload-excel/ URL’i eklenir.Varsayılan admin url'leri sadece nesnesi oluşturulan
model için oluşturulmaktadır. Örneğin; `model_examp` isimli bir modelin varsayılan URL listesi + `custom_urls` dediğimiz bizim kendi URL yapımız
döndürülür.

### redirect\_to\_upload\_excel

```python
def redirect_to_upload_excel(self, request):
```

Kullanıcıyı `customs_general` uygulamasındaki `upload_excel` view’ine yönlendirir.

## Toplu Model Kaydı

```python
models = apps.get_app_config("customs_general").get_models()

for model in models:
    admin.site.register(model, CustomAdmin)
```

Uygulamadaki tüm modeller admin paneline tek seferde kaydedilir. Her biri CustomAdmin davranışlarını kullanır.

## Özellik Özeti

| Özellik                   | Açıklama                                                |
| ------------------------- | ------------------------------------------------------- |
| Otomatik arama alanları   | CharField ve TextField alanları otomatik olarak eklenir |
| Autocomplete desteği      | FK ve M2M alanlar için otomatik autocomplete sağlanır   |
| Form alanı gizleme        | Belirli modele özel koşullu alan gizleme                |
| Excel ile veri yükleme    | Admin üzerinden butonla veri yükleme yönlendirmesi      |
| Dinamik URL yönlendirmesi | upload-excel/ → ilgili view                             |
| Toplu model kaydı         | Tüm modeller for döngüsü ile kaydedilir                 |

## Notlar

* admin/excel\_upload.html şablonu özel olarak tanımlanmıştır.
* Yapı başka uygulamalara da kolayca uyarlanabilir.
* Kod tekrarını azaltan ve merkezi kontrol sunan bir mimari önerir.
