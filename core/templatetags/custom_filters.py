from django import template
from core.constants import FK_M2M_REPRESENTATIVE_FIELDS

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

    # Eğer değer bir ForeignKey ise
    if hasattr(value, "_meta"):
        model_name = value.__class__.__name__
        representative_field = FK_M2M_REPRESENTATIVE_FIELDS.get(model_name)
        if representative_field:
            rep_value = getattr(value, representative_field, None)
            if rep_value:
                return f'<button class="btn btn-outline-primary btn-sm" style="margin:2px;"' \
                       f' onclick="openModelDetail(\'{model_name}\', {value.pk})">{rep_value}</button>'

        return str(value)

    # Eğer ManyToMany alanıysa (list gibi ise)
    if hasattr(value, "all"):
        model_name = value.model.__name__
        representative_field = FK_M2M_REPRESENTATIVE_FIELDS.get(model_name)
        if representative_field:
            reps = []
            for item in value.all():
                rep_value = getattr(item, representative_field, None)
                if rep_value:
                    reps.append(
                        f'<button class="btn btn-outline-primary btn-sm" style="margin:2px;" '
                        f'onclick="openModelDetail(\'{model_name}\', {item.pk})">{rep_value}</button>')

            return ", ".join(reps)
        return ", ".join([str(item) for item in value.all()])

    # Normal field
    return value
