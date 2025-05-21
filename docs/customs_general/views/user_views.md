# customs\_general/views/user\_views.py Dokümantasyonu

Bu belge, `customs_general/views/user_views.py` dosyasında bulunan view sınıflarının amacını, kullanım mantığını ve genel yapısını açıklar.

## Genel Amaç

Bu dosya, customs\_general uygulaması altında, kullanıcı (müşteri veya müşavir) arayüzü tarafından erişilecek tanım verilerini listeleyen view sınıflarını içerir. View yapısı, model adına göre dinamik olarak çalışır ve geliştirici tarafından her model için ayrı view yazma ihtiyacını ortadan kaldırır.

---

## GeneralCustomsModelListView Sınıfı

### Amaç

`customs_general` uygulamasındaki tüm tanım modelleri için, genel listeleme ve detay sorgulama view yapısı sunar.

### Bileşenler

* `app_label`: Uygulama etiketi ("customs\_general")
* `model_param`: URL veya GET parametresinden model adını alır
* `template_name`: Kullanılacak HTML şablon yolu
* `excluded_fields`: Listeden hariç tutulacak ortak alanlar

### dispatch(request, \*args, \*\*kwargs)

View çalışmadan önce gelen model adına göre `apps.get_model` ile dinamik model belirler. Model bulunamazsa "model not found" şablonunu render eder.

### get(request, \*args, \*\*kwargs)

* `?detail=1` GET parametresi varsa ilgili nesnenin detayı JSON olarak dönülür
* Aksi halde listeleme yapılır (super().get)

### Kullanım Senaryosu

Bu sınıf, tanımsal veri içeriklerinin (CurrencyType, Country, City vb.) listelenmesi veya detaylarının JSON olarak dönmesi gibi işlemlerde kullanılmak üzere tasarlanmıştır. Tüm modelleri için tek bir view yapısı kullanılarak tekrar eden kod yazımını azaltır.

---

## Yapısal Değerlendirme

* View sınıfı, gelişmiş bir GenericFilteredListView yapısından türetildiği için arama, filtreleme, pagination gibi işlevleri miras alarak yalın bir koda sahiptir.
* Dinamik model yönetimi sayesinde view yazım süreci sadeleştirilmiştir.
* Tek HTML şablon kullanarak tüm modeller için ortak bir arayüz sunulması hedeflenmiştir.

---

Bu doküman, `user_views.py` altında bulunan view'ların genel yapısını ve amacını özetlemektedir. Yeni view sınıfları eklenmesi durumunda benzer mantıkla yorumlanabilir.
