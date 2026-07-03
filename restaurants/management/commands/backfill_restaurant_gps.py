"""Set GPS coordinates on active restaurants that are missing them."""

from django.core.management.base import BaseCommand

from restaurants.models import Restaurant

CITY_COORDS = {
    Restaurant.City.RAMALLAH: (31.903800, 35.203400),
    Restaurant.City.GAZA: (31.501700, 34.466700),
    Restaurant.City.JERUSALEM: (31.768300, 35.213700),
    Restaurant.City.NABLUS: (32.221100, 35.254400),
    Restaurant.City.BETHLEHEM: (31.705400, 35.202400),
    Restaurant.City.JERICHO: (31.866700, 35.450000),
}


class Command(BaseCommand):
    help = "Backfill latitude/longitude for active restaurants using city defaults."

    def handle(self, *args, **options):
        updated = 0
        for restaurant in Restaurant.objects.filter(
            status=Restaurant.Status.ACTIVE,
            latitude__isnull=True,
        ):
            coords = CITY_COORDS.get(restaurant.city)
            if not coords:
                continue
            restaurant.latitude, restaurant.longitude = coords
            restaurant.save(update_fields=["latitude", "longitude"])
            updated += 1
            self.stdout.write(f"  {restaurant.name_en}: {coords}")

        self.stdout.write(self.style.SUCCESS(f"Updated {updated} restaurant(s)."))
