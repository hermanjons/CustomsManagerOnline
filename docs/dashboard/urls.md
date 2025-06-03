# 🔍 `dashboard/urls.py` Açıklaması

Bu dosya, `dashboard` uygulaması için URL tanımlarını içerir. Django'nun `urlpatterns` yapısı sayesinde bu uygulamaya ait giriş noktaları tanımlanır.

---

## Yapı

```python
from django.urls import path
from .views import dashboard_home

urlpatterns = [
    path('', dashboard_home, name='dashboard_home'),
]
```

### Öğe 1: `''`

* Bu, dashboard uygulaması için **ana URL**’yi belirtir.
* Örnek: `/dashboard/` adresine gidildiğinde `dashboard_home` view fonksiyonu çağrılır.

### Öğe 2: `dashboard_home`

* View fonksiyonu olarak tanımlanır.
* Ana panelin anasayfasını oluşturur.
* kendi dökümanlarında detaylı bilgi bulabilirsiniz

### Öğe 3: `name='dashboard_home'`

* Bu URL çıktısı için bir **isim tanımı** yapar.
* Template içinde veya `reverse()` fonksiyonunda `url 'dashboard_home'` olarak kullanılabilir.

---

Bu yapı, proje genel URL yapısında `include("dashboard.urls")` ile entegre edilerek `/dashboard/` gibi bir alt yol üzerinden aktif edilir.

**Örnek Proje URL'leri:**

```python
path("dashboard/", include("dashboard.urls"))
```

Bu sayede `/dashboard/` adresi, `dashboard_home` view'ine yönlendirilir.
