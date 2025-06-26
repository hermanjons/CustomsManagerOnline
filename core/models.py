from django.db import models
from core.utils.context_utils import get_current_user
from django.conf import settings
import uuid
from .utils.utils import date_based_upload_path


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class AuditModel(TimeStampedModel, SoftDeleteModel):
    custom_model = True

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_created_by'
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='%(class)s_updated_by'
    )

    record_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    system_note = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        user = get_current_user()
        print("Kullanıcı:", user)

        if self._state.adding:
            print("ilk kayıt")
            if user:
                self.created_by = user
        else:
            if user:
                self.updated_by = user

        super().save(*args, **kwargs)


class AuditModelWithId(AuditModel):
    id = models.IntegerField(primary_key=True)

    class Meta:
        abstract = True


class AuditModelWithSource(AuditModel):
    data_source = models.ForeignKey(
        "customs_general.DataSource", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        abstract = True


class AuditModelWithIdAndSource(AuditModelWithSource, AuditModelWithId):
    class Meta:
        abstract = True


class UploadedDocumentsBase(AuditModelWithSource):
    doc_name = models.CharField(max_length=255)
    doc_file = models.FileField(upload_to=date_based_upload_path)

    def __str__(self):
        return f"{self.doc_name}"

    class Meta:
        verbose_name = "Yüklenen Dökümanlar"
        verbose_name_plural = "Yüklenen Dökümanlar"
