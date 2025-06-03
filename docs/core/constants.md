# 📌 `core/constants.py` Açıklaması

Bu dosya, projede yaygın olarak kullanılan bazı sabit (constant) sözlük yapılarını içerir. UI/UX geliştirme, veri eşleştirme ve form alanlarının düzgün gösterimi gibi amaçlarla kullanılır.

---

## 1. `MODEL_ICONS`

* Her bir veri modeline karşılık gelen **emoji ikonlarını** tanımlar.
* Amaç: Arayüzde kullanıcıya daha görsel bir deneyim sunmak.
* Örnek: `"country": "🌎"` — Ülke modeline dünya emojisi atanmış.

---

## 2. `MODEL_FIELD_VERBOSE_NAMES`

* Her modelin alanları (field) için **görünen adları** içerir.
* Amaç: Admin paneli veya formlarda alan adlarını kullanıcı dostu hale getirmek.
* Türkçe ve İngilizce açıklamaları içerebilir.
* Örnek:

  ```python
  'country': {
      'country_code_alpha2': 'Ülke Kodu (Alpha-2)',
      'country_name_tr': 'Ülke Adı (TR)'
  }
  ```

---

## 3. `FK_M2M_REPRESENTATIVE_FIELDS`

* ForeignKey ve ManyToMany alanlarında hangi alanın temsil edici (gösterilecek) olduğunu belirtir.
* Amaç: Dropdown, autocomplete vb. alanlarda hangi alan gösterilecekse onu tanımlamak.
* Örnek: `"Country": "country_name_tr"` — Country modelinde ülkenin Türkçe adı gösterilir.

---

Bu yapı, projedeki modellerin sade, anlaşılır ve yönetilebilir biçimde kullanıcı arayüzüne yansıtılmasını sağlar.
