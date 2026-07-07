"""Set GPS coordinates on active restaurants that are missing them."""

from django.core.management.base import BaseCommand

from restaurants.geo import CITY_DEFAULT_COORDS
from restaurants.models import Restaurant


class Command(BaseCommand):
    help = "Backfill latitude/longitude for active restaurants using city defaults."

    def handle(self, *args, **options):
        updated = 0
        for restaurant in Restaurant.objects.filter(
            status=Restaurant.Status.ACTIVE,
            latitude__isnull=True,
        ):
            coords = CITY_DEFAULT_COORDS.get(restaurant.city)
            if not coords:
                continue
            restaurant.latitude, restaurant.longitude = coords
            restaurant.save(update_fields=["latitude", "longitude"])
            updated += 1
            self.stdout.write(f"  {restaurant.name_en}: {coords}")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} restaurant(s)."))
