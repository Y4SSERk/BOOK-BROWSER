from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User, Profile  

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Signal handler to create user profile and default shelves when a new user is created"""
    if created:
        profile = Profile.objects.create(user=instance)
        profile.create_default_shelves()