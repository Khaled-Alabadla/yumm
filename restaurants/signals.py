"""Restaurant model signals."""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Restaurant
from .owner_sync import sync_owner_approval


@receiver(pre_save, sender=Restaurant)
def store_previous_restaurant_status(sender, instance: Restaurant, **kwargs):
    """Remember prior status so we can detect approval transitions."""
    if not instance.pk:
        instance._previous_status = None
        return
    previous = (
        Restaurant.objects.filter(pk=instance.pk)
        .values_list("status", flat=True)
        .first()
    )
    instance._previous_status = previous


@receiver(post_save, sender=Restaurant)
def sync_owner_after_restaurant_save(sender, instance: Restaurant, **kwargs):
    sync_owner_approval(instance)

    # Admin / actions may send the email themselves and set this flag.
    if getattr(instance, "_skip_approval_email", False):
        return

    previous = getattr(instance, "_previous_status", None)
    became_active = (
        instance.status == Restaurant.Status.ACTIVE
        and previous != Restaurant.Status.ACTIVE
        and instance.owner_id
    )
    if not became_active:
        return

    from accounts.emails import send_owner_approved_email

    owner = instance.owner
    if owner is not None:
        send_owner_approved_email(owner, instance)
