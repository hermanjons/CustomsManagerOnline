from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


# Kullanıcı oluşturma yöneticisi
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


# Asıl kullanıcı modeli
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Admin'
        CONSULTANT = 'consultant', 'Consultant'
        CLIENT = 'client', 'Client'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.ADMIN)

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if self.role == 'admin':
            self.is_staff = True
        else:
            self.is_staff = False  # admin değilse panelden uzak dur!
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.username} ({self.role})"


class ConsultantProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultant_profile')

    full_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    iban = models.CharField(max_length=34, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} ({self.company_name})"


class ClientProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_profile')

    company_name = models.CharField(max_length=255)
    authorized_person = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    iban = models.CharField(max_length=34, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    tax_number = models.CharField(max_length=20, blank=True, null=True)
    consultants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="consulted_clients",
        limit_choices_to={'role': 'consultant'},
        blank=True
    )


    def __str__(self):
        return f"{self.company_name}"
