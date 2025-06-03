from django.core.cache import cache


def clear_user_cache_keys(user_id, *keys, namespace=None):
    """
    Belirli kullanıcıya ait cache anahtarlarını siler.

    Args:
        user_id (int): Kullanıcı ID'si
        *keys (str): Anahtar adları (örneğin: 'upload_progress', 'failed_rows')
        namespace (str): Varsayılan olarak ön ek (örn: app adı)
    """
    for key in keys:
        full_key = f"{namespace + ':' if namespace else ''}{key}:{user_id}"
        cache.delete(full_key)


def set_user_cache_key_if_changed(user_id, key, value, timeout=300, namespace=None):
    full_key = f"{namespace + ':' if namespace else ''}{key}:{user_id}"
    current = cache.get(full_key)
    if current != value:
        cache.set(full_key, value, timeout=timeout)
