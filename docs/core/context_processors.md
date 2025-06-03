# 📜 `core/context_processors.py` Açıklaması

Bu dosya, Django projesi içerisinde şablonlara (template'lere) **global context verileri** sağlamak için kullanılır. Buradaki fonksiyonlar sayesinde, her sayfada tekrar tekrar veri göndermek yerine genel veriler otomatik olarak template'lere aktarılabilir.

---

## 1. `model_list(request)`

Bu fonksiyon, şu amaçla kullanılır:

* Yüklenen uygulamalardaki modelleri listeler.
* Bunları 3 gruba ayırır:

  * `genel_tanimlamalar_models` → `customs_general` uygulamasından gelenler
  * `urun_islemleri_models` → `products` uygulamasından gelenler
  * `diger_models` → önceden belirlenen `DIGER_MODELLER` listesine göre seçilir
* Her model için:

  * Model adı (`model_name`)
  * Görüntülenecek ad (`verbose_name`)
  * Emoji ikonu (`MODEL_ICONS` içinden)

içeren bir context objesi döner.

**Template'te Kullanım Amaçları**:

* Sidebar menülerinde dinamik olarak modellerin listelenmesi
* Otomatik ikon ve isim gösterimi

---

## 2. `site_logo_release(request)`

Bu fonksiyon, şablonlara **site logosu** bilgisi sağlar.

* `settings.SITE_LOGO` değeri var ise, bu logo static dizininden kullanılır.
* Aksi halde varsayılan olarak `static/onlinecustoms.png` döner.

**Amaç:**

* Tüm sayfalarda ön tanımlı bir logo kullanımını merkezi olarak yönetmek.

**Kullanım Alanları**:

* Navbar'da site logosu gösterimi
* Admin panel branding

---

Bu dosya, projedeki şablonlara merkezi olarak bilgi aktarmak için kullanılması gereken önemli bir yapıdır. Yeni context fonksiyonları eklemek için bu yapı referans alınabilir.
