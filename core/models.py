from django.db import models


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
    custom_model = True  # Tüm custom modellerde sistemsel olarak işaretli olur

    class Meta:
        abstract = True


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
