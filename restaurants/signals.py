"""Restaurant model signals."""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Restaurant
from .owner_sync import sync_owner_approval


@receiver(post_save, sender=Restaurant)
def sync_owner_after_restaurant_save(sender, instance: Restaurant, **kwargs):
    sync_owner_approval(instance)
