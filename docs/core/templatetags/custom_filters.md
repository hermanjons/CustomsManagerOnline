# 🌐 `core/templatetags/custom_filters.py` Açıklaması

Bu dosya, Django template sisteminde kullanılmak üzere özel filtreler tanımlar. Projenin genelinde tekrar eden veri gösterimleri veya field üzerinden çekim işlemleri gibi ihtiyaçları karşılamak amacıyla `core` içerisine yerleştirilmiştir.

---

## 1. `getattr_custom`

```python
@register.filter(name='getattr_custom')
def getattr_custom(obj, attr_name):
```

* Bir nesneden dinamik olarak alan değeri çeker.
* Eğer alan ManyToMany ise `.all()` sonucu listeye çevrilerek dönülür.
* Template içinde `join` gibi işlemlerde kullanılabilir.

**Örnek Kullanım:**

```django
{{ object|getattr_custom:"alan_adi" }}
```

---

## 2. `get_dict_value`

```python
@register.filter(name="get_dict_value")
def get_dict_value(dictionary, key):
```

* Bir sözlükten (dict) değer çeker.
* Eğer key bulunamazsa, key'in kendisini döner.
* Template tarafında özellikle verbose name haritalaması gibi alanlarda kullanılabilir.

**Örnek Kullanım:**

```django
{{ model_field|get_dict_value:field_key }}
```

---

## 3. `render_field`

```python
@register.filter
def render_field(obj, field_name):
```

* Dinamik olarak bir model alanını çeker ve HTML çıktı verir.
* Özellikle ForeignKey ve ManyToManyField alanlar için **buton formatında** görsel temsil sağlar.
* `FK_M2M_REPRESENTATIVE_FIELDS` sabiti yardımıyla hangi alanın temsil edileceğine karar verir.
* Tüm alanlar için fallback olarak string dönüş sağlanır.

**Özellikleri:**

* FK: Temsil edici field üzerinden butonlu temsil
* M2M: Tüm öğeleri butonlu olarak listeler
* Diğer: Değeri string olarak döner

**Örnek HTML dönüşü:**

```html
<button class="btn btn-outline-primary btn-sm" onclick="openModelDetail('Country', 1)">Türkiye</button>
```

---

Bu filtreler, uygulama bağımsız çalışacak şekilde tasarlanmıştır ve bu nedenle `core/templatetags/` içerisinde bulunması mantıklıdır. Özelleşmiş templatetag filtreleri ihtiyacınızda buraya yenilerini ekleyebilirsiniz.
