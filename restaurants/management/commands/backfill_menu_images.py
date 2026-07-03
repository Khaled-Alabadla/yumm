"""Copy local static dish photos into menu item uploads."""

from pathlib import Path

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from restaurants.constants import DISHES_DIR, resolve_dish_image_file
from restaurants.models import MenuItem


class Command(BaseCommand):
    help = "Attach local dish photos to menu items missing an image."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace existing menu item images.",
        )

    def handle(self, *args, **options):
        attached = 0
        for item in MenuItem.objects.all():
            if item.image and not options["force"]:
                continue
            filename = resolve_dish_image_file(item.name_en)
            source = DISHES_DIR / filename
            if not source.exists():
                self.stdout.write(self.style.WARNING(f"Missing static file: {filename}"))
                continue
            if item.image:
                item.image.delete(save=False)
            data = source.read_bytes()
            item.image.save(filename, ContentFile(data), save=True)
            attached += 1
        self.stdout.write(self.style.SUCCESS(f"Attached photos to {attached} menu items."))
