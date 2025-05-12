import os
from datetime import datetime


def date_based_upload_path(instance, filename):
    """
    Dosyaları, 'uploads/YYYY/MM/DD/' yapısına göre kaydeder ve
    dosya adını tarih-saat bilgisi ile benzersiz hale getirir.
    """
    ext = filename.split('.')[-1]
    new_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.{ext}"
    return os.path.join('uploads', datetime.now().strftime('%Y/%m/%d'), new_filename)