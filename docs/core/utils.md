# 📁 `core/utils.py` Açıklaması

Bu dosya, projede genel olarak kullanılabilecek **yardımcı (utility)** fonksiyonları içerir. Tek bir amaca hizmet eden küçük ama kullanışlı yapılar burada tutulur.

---

## 1. `date_based_upload_path(instance, filename)`

**Amaç:**

* Dosyaları tarih bazlı klasörlere kaydetmek ve isim çakışmasını önlemek.

**Yapı:**

* Dosya yolu: `uploads/YYYY/MM/DD/`
* Dosya adı: `YYYYMMDD_HHMMSS.ext` formatında benzersiz ad verilir.

**Parametreler:**

* `instance`: Model instance'ı (Django tarafından otomatik verilir).
* `filename`: Orijinal dosya adı.

**Dönüş:**

```python
'uploads/2025/05/21/20250521_101234.pdf'
```

**Kullanım Alanları:**

* Django modellerinde `upload_to=` alanlarında kullanılabilir.

**Örnek Kullanım:**

```python
class UploadedDocument(models.Model):
    file = models.FileField(upload_to=date_based_upload_path)
```

---

Bu fonksiyon, düzgün bir dosya organizasyonu ve isim çakışmasını önleme için pratik bir yöntem sunar.
