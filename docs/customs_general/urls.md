# customs\_general/urls.py Belgelendirme

Bu dosya, `customs_general` uygulamasına ait URL yönlendirmelerini tanımlar. Uygulama, genel gümrük tanımlamalarıyla ilgili veri yönetimi, Excel yükleme, yükleme ilerleme takibi ve başarısız satırların indirilmesi gibi işlemleri desteklemektedir.

## Namespace

```python
app_name = 'customs_general'
```

Bu satır sayesinde bu uygulamadaki URL isimleri diğer uygulamalardan ayrıştırılabilir hale gelir. Örneğin, `reverse('customs_general:upload_excel', args=[model_name])` gibi kullanılabilir.

## URL Tanımları

### 1. Model Verileri Listeleme

```python
path('<str:model>/', GeneralCustomsModelListView.as_view(), name='model_data')
```

* Genel tanım modellerini listelemek için kullanılır.
* Dinamik olarak `str:model` parametresi alır (örneğin `Country`, `CurrencyType` gibi).
* URL sıralamsına dikkat edilmelidir.liste içerisinde en başta yazılırsa hata alınabilir.
* URL sıralamsında bu tip URL tanımlamaları en sona yazılmalıdır.

### 2. Excel ile Veri Yükleme

```python
path('upload-excel/<str:model>/', upload_excel, name="upload_excel")
```

* Belirli bir modele ait verileri Excel dosyası ile sisteme yükler.
* Model ismi URL'den dinamik alınır.

### 3. Yükleme İlerleme Durumu

```python
path('upload-progress/', upload_progress, name='upload_progress')
```

* Asenkron veri yüklemelerinde yükleme durumunu göstermek için kullanılır.
* JavaScript tarafından periyodik olarak sorgulanabilir.

### 4. Başarısız Satırları İndirme

```python
path('download-failed-rows/<str:model>/', download_failed_rows, name='download_failed_rows')
```

* Excel yüklemesi sırasında hatalı bulunan satırların tekrar incelenmesi için indirilmesini sağlar.

### 5. Belirli Nesne Detayını Getirme

```python
path('fetch-model-detail/<str:model>/<int:pk>/', GeneralCustomsModelListView.as_view(), name='fetch_model_detail')
```

* Belirli bir modele ve ID’ye karşılık gelen nesnenin detayını döndürür.
* Genellikle AJAX ile detaylı veri çekme senaryolarında kullanılır.
* yapısal olarak `model_data` isimli URL ile farklı bir iş yapmamaktadır.
* Tek fark ID değerine karşılık gelen veriyi döndürmesidir.

## Genel Kullanım Senaryosu

Bu yapı ile `customs_general` uygulamasındaki birçok model için ortak bir URL ve view yapısı oluşturulmuş olur. Dinamik model adı sayesinde aynı yapı tüm modeller için tekrar kullanılabilir hale gelir.

Bu, merkezi ve sürdürülebilir bir URL mimarisi sağlar.
