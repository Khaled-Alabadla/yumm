"""Attach local static dish photos to menu items."""

from django.core.files.base import ContentFile

from .constants import DISHES_DIR, resolve_dish_image_file


def attach_menu_item_image(item, *, force: bool = False) -> bool:
    """Copy an authentic dish photo from static files onto the menu item."""
    if item.image and not force:
        return True

    filename = resolve_dish_image_file(item.name_en)
    source = DISHES_DIR / filename
    if not source.exists():
        for fallback in ("musakhan.jpg", "mansaf.jpg", "maqluba.jpg", "knafeh.jpg", "shawarma.jpg"):
            candidate = DISHES_DIR / fallback
            if candidate.exists():
                source = candidate
                filename = fallback
                break
        else:
            return False

    if item.image:
        item.image.delete(save=False)

    item.image.save(filename, ContentFile(source.read_bytes()), save=True)
    return True
