# `products/admin.py` Açıklaması

Bu dosya, `products` uygulamasındaki tüm modellerin Django admin paneline otomatik olarak kayıt edilmesini sağlar. Normalde her model için tek tek `admin.site.register(ModelAdı)` yazmak gerekirken, bu yapı ile tüm modeller dinamik olarak yüklenir.

---

## Kod İçeriği:

```python
from django.contrib import admin
from django.apps import apps

models = apps.get_app_config("products").get_models()

for model in models:
    admin.site.register(model)
```

---

## Ne Yapar?

* `apps.get_app_config("products")`: `products` uygulamasının konfigürasyonunu getirir.
* `.get_models()`: Bu uygulamadaki tüm modelleri listeler.
* `for model in models`: Her model üzerinden dönerek admin'e kaydeder.

---

## Avantajlar:

* Daha az kod, daha az tekrar
* Yeni model eklediğinde admin.py dosyasına elle bir şey yazmana gerek kalmaz
* Zaman kazandırır ve geliştirme hızını artırır

---

## Dikkat Edilmesi Gerekenler:

* Özel `ModelAdmin` tanımları yapacaksan bu yöntem yerine admin sınıfını override ederek customize edilmiş sınıfı yazdırabiliriz.
* Admin'de her modelin görünmesini istemediğin durumlarda bu yöntem uygun olmayabilir.

---

Bu yapı, admin panelini otomatikleştirerek geliştirme sürecini kolaylaştırmak için pratik bir yöntemdir. Tek bir satırla tüm modelleri aktif hale getirir.
