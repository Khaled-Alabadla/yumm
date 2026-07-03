"""Download one unique restaurant cover per demo restaurant (no people)."""

import subprocess
import time
from pathlib import Path

# Wikimedia Commons title -> local slug filename
COVERS = {
    "Interior of glamorous restaurant.jpg": "al-kanaan.jpg",
    "Charcoal_grill.jpg": "gaza-grill-house.jpg",
    "An empty table in a restaurant.jpg": "jerusalem-garden-cafe.jpg",
    "Boulangerie.jpg": "nablus-sweets-house.jpg",
    "Cake_shop.jpg": "bethlehem-zaatar-oven.jpg",
    "Steak_house.jpg": "jericho-dates-grill.jpg",
    "Dishoom King's Cross interior 4.jpg": "al-sham-kitchen.jpg",
    "Mario's interior.jpg": "hebron-heritage-kitchen.jpg",
    "Interior of restaurant Faro in Ruoholahti, Helsinki.jpg": "gaza-mediterranean-blue.jpg",
    "Interior of a dining area.jpg": "ramallah-sweet-palace.jpg",
    "Hotel Interlaken Interior Restaurant.jpg": "jerusalem-shawarma-express.jpg",
}

OUT = Path(__file__).resolve().parent
UA = "YummDemo/1.0"
WIDTH = 1200


def download(commons_name: str, dest: Path) -> bool:
    encoded = commons_name.replace(" ", "%20").replace("'", "%27")
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width={WIDTH}"
    result = subprocess.run(
        ["curl.exe", "-L", "-A", UA, "-o", str(dest), "-w", "%{http_code}", url],
        capture_output=True,
        text=True,
        timeout=120,
    )
    code = (result.stdout or "").strip()[-3:]
    if code != "200" or not dest.exists() or dest.stat().st_size < 8000:
        dest.unlink(missing_ok=True)
        return False
    if dest.read_bytes()[:15].lstrip().startswith(b"<!"):
        dest.unlink(missing_ok=True)
        return False
    return True


def main() -> None:
    for commons_name, filename in COVERS.items():
        dest = OUT / filename
        print(f"fetch {filename} …", end=" ")
        time.sleep(2)
        ok = download(commons_name, dest)
        print("ok" if ok else "FAILED")


if __name__ == "__main__":
    main()
