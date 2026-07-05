"""Keep owner accounts in sync with their restaurant approval status."""

from __future__ import annotations

from accounts.models import CustomUser

from .models import Restaurant


def sync_owner_approval(restaurant: Restaurant) -> None:
    """
    Mirror restaurant.status onto the linked owner account.

    Active restaurant   → owner can sign in
    Pending / rejected  → owner stays blocked
    """
    if not restaurant.owner_id:
        return

    owner_qs = CustomUser.objects.filter(
        pk=restaurant.owner_id,
        role=CustomUser.Role.OWNER,
    )

    if restaurant.status == Restaurant.Status.ACTIVE:
        owner_qs.update(is_approved=True, is_active=True)
    elif restaurant.status == Restaurant.Status.REJECTED:
        owner_qs.update(is_approved=False, is_active=False)
    elif restaurant.status == Restaurant.Status.PENDING:
        owner_qs.update(is_approved=False)


def sync_restaurants_for_owner(owner: CustomUser) -> None:
    """When an owner account is approved manually, activate their restaurants."""
    if not owner.is_owner_role:
        return

    if owner.is_approved and owner.is_active:
        Restaurant.objects.filter(owner=owner).update(
            status=Restaurant.Status.ACTIVE,
            is_open=True,
        )
    elif not owner.is_approved or not owner.is_active:
        Restaurant.objects.filter(owner=owner).exclude(
            status=Restaurant.Status.REJECTED,
        ).update(status=Restaurant.Status.PENDING, is_open=False)


def owner_has_active_restaurant(owner: CustomUser) -> bool:
    return Restaurant.objects.filter(
        owner=owner,
        status=Restaurant.Status.ACTIVE,
    ).exists()
