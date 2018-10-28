from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta

from models3d.models import Model
from .models import Pioneer, Collector, Star

@receiver(post_save, sender=User)
def on_user_save(sender, instance, created, **kwargs):
    if created:
        active_date = instance.date_joined + timedelta(days=365)
        Pioneer.objects.create(user=instance, active_on=active_date)

@receiver(post_save, sender=Model)
def on_model_save(sender, instance, update_fields, created, **kwargs):
    if created and instance.user.models.count() == 5:
        Collector.objects.get_or_create(user=instance.user)
    
    if update_fields and 'views' in update_fields and instance.views == 100:
        Star.objects.get_or_create(user=instance.user, defaults={'model': instance})
