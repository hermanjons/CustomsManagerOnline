# 🌐 `dashboard/views.py` Açıklaması

Bu dosya, `dashboard` uygulamasına ait görüntülemeleri (views) barındırır. şu an için yalnızca ana sayfa görüntülemesi yer almaktadır.

---

## 1. `dashboard_home(request)`

```python
def dashboard_home(request):
    return render(request, 'dashboard/index.html')
```

### Amaç:

* `/dashboard/` adresine gelindiğinde çalışan **anasayfa view fonksiyonudur**.
* Template olarak `dashboard/index.html` dosyasını render eder.

### Parametre:

* `request`: HTTP isteği nesnesi (kullanıcıdan gelen bilgi)

### Dönüş:

* `render(...)` fonksiyonu ile HTML şablonunu cevap olarak döner.

### Bağlı Dosyalar:

* HTML: `templates/dashboard/index.html`
* URL: `dashboard/urls.py` üzerinden path tanımlı

---

Bu yapı, dashboard bölümünü başlatacak ilk yüzeydir ve ileride verilerle zenginleştirilebilir (istatistik kutuları, grafikler, bildirimler vb.).
