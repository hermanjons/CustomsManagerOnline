from django import template

register = template.Library()


@register.filter
def getattr_custom(obj, attr_name):
    return getattr(obj, attr_name, None)


@register.filter(name="get_dict_value")
def get_dict_value(dictionary, key):
    """Sözlük içinden güvenli şekilde değer alır, eğer yoksa key'i döner."""
    return dictionary.get(key, key)
