"""Map defaults and city coordinates for Palestine."""

from __future__ import annotations

from restaurants.models import Restaurant

# Default center (Ramallah) when no city match exists.
PALESTINE_CENTER = (31.903800, 35.203400)
PALESTINE_MAP_ZOOM = 9
LOCATION_PICKER_ZOOM = 15

# West Bank + Gaza bounding box.
PALESTINE_LAT_MIN = 31.0
PALESTINE_LAT_MAX = 33.5
PALESTINE_LNG_MIN = 34.0
PALESTINE_LNG_MAX = 35.9

CITY_DEFAULT_COORDS: dict[str, tuple[float, float]] = {
    Restaurant.City.RAMALLAH: (31.903800, 35.203400),
    Restaurant.City.GAZA: (31.501700, 34.466700),
    Restaurant.City.JERUSALEM: (31.768300, 35.213700),
    Restaurant.City.NABLUS: (32.221100, 35.254400),
    Restaurant.City.BETHLEHEM: (31.705400, 35.202400),
    Restaurant.City.JERICHO: (31.866700, 35.450000),
    Restaurant.City.HEBRON: (31.532600, 35.099800),
    Restaurant.City.JENIN: (32.460700, 35.300000),
    Restaurant.City.TULKARM: (32.310800, 35.028600),
    Restaurant.City.QALQILYA: (32.189600, 34.970600),
    Restaurant.City.SALFIT: (32.083900, 35.173600),
    Restaurant.City.TUBAS: (32.320900, 35.369400),
}


def is_valid_palestine_coords(lat, lng) -> bool:
    """Return True when coordinates fall inside Palestine (West Bank + Gaza)."""
    try:
        lat_f = float(lat)
        lng_f = float(lng)
    except (TypeError, ValueError):
        return False
    return (
        PALESTINE_LAT_MIN <= lat_f <= PALESTINE_LAT_MAX
        and PALESTINE_LNG_MIN <= lng_f <= PALESTINE_LNG_MAX
    )


def get_restaurant_map_defaults(restaurant) -> tuple[float, float, int]:
    """Return lat, lng, zoom for the dashboard location picker."""
    if (
        restaurant.latitude is not None
        and restaurant.longitude is not None
        and is_valid_palestine_coords(restaurant.latitude, restaurant.longitude)
    ):
        return (
            float(restaurant.latitude),
            float(restaurant.longitude),
            LOCATION_PICKER_ZOOM,
        )
    coords = CITY_DEFAULT_COORDS.get(restaurant.city)
    if coords:
        return coords[0], coords[1], LOCATION_PICKER_ZOOM
    return PALESTINE_CENTER[0], PALESTINE_CENTER[1], PALESTINE_MAP_ZOOM


def get_all_city_choices() -> list[tuple[str, str]]:
    """All Palestine cities sorted by display label."""
    return sorted(Restaurant.City.choices, key=lambda item: str(item[1]))
