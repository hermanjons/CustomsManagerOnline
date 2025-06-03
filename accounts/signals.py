from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, ClientProfile, ConsultantProfile

@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == CustomUser.Role.CLIENT:
            ClientProfile.objects.create(user=instance, email=instance.email)
        elif instance.role == CustomUser.Role.CONSULTANT:
            ConsultantProfile.objects.create(user=instance, email=instance.email)
