from django import template
from core.constants import FK_M2M_REPRESENTATIVE_FIELDS
from django.db import models
register = template.Library()


@register.filter(name='getattr_custom')
def getattr_custom(obj, attr_name):
    try:
        value = getattr(obj, attr_name)
        # ManyToManyField ise .all() çağır
        if hasattr(value, 'all'):
            return list(value.all())  # liste yapıyoruz ki template içinde join çalışsın
        return value
    except AttributeError:
        return None


@register.filter(name="get_dict_value")
def get_dict_value(dictionary, key):
    """Sözlük içinden güvenli şekilde değer alır, eğer yoksa key'i döner."""
    return dictionary.get(key, key)


@register.filter
def render_field(obj, field_name):
    value = getattr(obj, field_name, None)

    try:
        field = obj._meta.get_field(field_name)
    except Exception:
        return value  # Eğer alan yoksa olduğu gibi döndür

    # 🔷 ForeignKey veya OneToOne
    if isinstance(field, (models.ForeignKey, models.OneToOneField)):
        if value is None:
            return "-"
        model_name = value.__class__.__name__
        representative_field = FK_M2M_REPRESENTATIVE_FIELDS.get(model_name)
        if representative_field:
            rep_value = getattr(value, representative_field, None)
            if rep_value:
                return f'<button class="btn btn-outline-primary btn-sm" style="margin:2px;" ' \
                       f'onclick="openModelDetail(\'{model_name}\', {value.pk})">{rep_value}</button>'
        return str(value)

    # 🔷 ManyToMany
    elif isinstance(field, models.ManyToManyField):
        model_name = field.related_model.__name__
        representative_field = FK_M2M_REPRESENTATIVE_FIELDS.get(model_name)
        if representative_field:
            reps = []
            for item in value.all():
                rep_value = getattr(item, representative_field, None)
                if rep_value:
                    reps.append(
                        f'<button class="btn btn-outline-primary btn-sm" style="margin:2px;" '
                        f'onclick="openModelDetail(\'{model_name}\', {item.pk})">{rep_value}</button>')
            return ", ".join(reps) or "-"
        return ", ".join([str(item) for item in value.all()]) or "-"

    # 🔷 Görsel (ImageField)
    elif isinstance(field, models.ImageField):
        if value:
            return f'<img src="{value.url}" class="img-thumbnail" style="max-width: 100px;">'
        return "-"

    # 🔷 Dosya (FileField)
    elif isinstance(field, models.FileField):
        if value:
            return f'<a href="{value.url}" target="_blank">📄 Dosyayı Aç</a>'
        return "-"

    # 🔷 Tarih/Saat formatı
    elif isinstance(field, (models.DateTimeField, models.DateField)):
        return value.strftime("%d.%m.%Y %H:%M") if value else "-"

    # 🔷 Normal değer
    return str(value) if value not in [None, ""] else "-"
