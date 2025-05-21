# customs\_general/views/admin\_views.py Dokümantasyonu

Bu belge, `customs_general/views/admin_views.py` dosyasındaki admin paneline özel geliştirilen view fonksiyonlarının amacını ve işlevlerini açıklar.

## Amaç

Bu dosya, sadece **personel (staff)** yetkisine sahip admin kullanıcıların kullanabileceği, özellikle Excel ile veri yükleme gibi işlemleri yöneten view fonksiyonlarını barındırır.

---

## upload\_excel(request, model)

### Amacı

Yönetici kullanıcı tarafından `.csv` veya `.xlsx` formatında Excel dosyası yüklenmesini sağlar. Dinamik olarak model adına göre veri kayıt eder.

### Ana Aşamalar

1. **Dosya tipi kontrolü**: Sadece `.csv` ve `.xlsx` uzantıları desteklenir.
2. **Model alanlarını al**: Tüm alanlar, `ForeignKey`, `ManyToMany` ve self-relation olanlar ayrı ayrı belirlenir.
3. **Zorunlu alanlar kontrol edilir**: Eksikse kayıt yapılmaz.
4. **Veriler yaratılır**:

   * 1. Aşama: Self-FK olmayan kayıtlar create edilir.
   * 2. Aşama: Self-FK alanlar temp id haritasından güncellenir.
5. **ManyToMany alanlar** string olarak virgülle ayrılmış id'lerle ayarlanır.
6. **cache** ile Redis'e yükleme ilerlemesi atanır: `upload_progress:{user_id}`
7. **request.session\['failed\_rows']** ile hata listesi tutulur.
8. **JsonResponse** döner.

### Yetkilendirme

Sadece `@staff_member_required` olan kullanıcılar erişebilir.

---

## upload\_progress(request)

### Amacı

Redis cache üzerinden yükleme sürecinin yüzde kaçı tamamlandığını frontend'e dönmek.

### İşleyişi

* `request.user.id` ile Redis key'i belirlenir
* Redis'ten `upload_progress:{user_id}` değeri getirilir
* `JsonResponse` olarak dönülür

### Özellik

Kullanıcı girişli değilse `progress: 0` + debug mesajı ile cevap verilir.

---

## download\_failed\_rows(request, model)

### Amacı

Excel yükleme sırasında hata alan satırları çıkarıp admin kullanıcıya indirme imkânı sunmak.

### İşleyişi

* `request.session['failed_rows']` kontrol edilir
* Satırlar `pandas.DataFrame`'e aktarılır
* `openpyxl` motoru ile Excel dosyasına yazılır
* `HttpResponse` şeklinde `.xlsx` dosyası dönülür

### Şart

Yine sadece staff üyeleri erişebilir (`@staff_member_required`)

---

## Yapısal Değerlendirme

| Özellik        | Açıklama                                                               |
| -------------- | ---------------------------------------------------------------------- |
| Dinamik Model  | `apps.get_model("customs_general", model)` ile modeli runtime'da bulur |
| Redis Progress | Gerçek zamanlı yükleme göstergesi için Redis kullanılır                |
| Hata Kaydı     | Session içinde hata satırları saklanır ve indirilebilir                |

---

Bu yapı, admin tarafından yapılan Excel yüklemelerinde, hem kullanıcı deneyimini artırır hem de işlem takibini frontend tarafından mümkün kılar.
