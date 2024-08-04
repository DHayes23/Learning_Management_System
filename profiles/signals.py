from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

"""
This function is triggered after a User instance is saved. It checks if the User instance is newly created
(created is True), and if so, it creates a corresponding Profile instance linked to the new User.
"""
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

"""
This function ensures that any changes made to a User instance also 
affect the Profile.
"""
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
