"""Remove auto-downloaded demo dish photos so static fallbacks are used."""

from django.core.management.base import BaseCommand

from restaurants.models import MenuItem


class Command(BaseCommand):
    help = "Clear menu item images (use static dish photos until owners upload their own)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Clear all menu item images, not only auto-seeded JPG names.",
        )

    def handle(self, *args, **options):
        qs = MenuItem.objects.exclude(image="")
        if not options["force"]:
            qs = qs.filter(image__regex=r"menu/items/.*\.jpg$")
        count = 0
        for item in qs.iterator():
            if item.image:
                item.image.delete(save=False)
                item.image = None
                item.save(update_fields=["image"])
                count += 1
        self.stdout.write(self.style.SUCCESS(f"Cleared {count} menu item images."))
