"""Check whether MySQL time zone tables are installed."""

from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = (
        "Verify MySQL time zone support. Required for admin date drill-down "
        "filters that use CONVERT_TZ()."
    )

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT CONVERT_TZ('2001-01-01 01:00:00', 'UTC', 'UTC') IS NOT NULL"
            )
            ok = bool(cursor.fetchone()[0])

        if ok:
            self.stdout.write(self.style.SUCCESS("MySQL time zone tables are installed."))
            return

        self.stdout.write(
            self.style.ERROR(
                "MySQL time zone tables are NOT installed. "
                "Admin date hierarchy / DateFieldListFilter will fail until they are loaded."
            )
        )
        self.stdout.write("")
        self.stdout.write("On Windows (adjust paths to your MySQL install):")
        self.stdout.write(
            r'  "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql_tzinfo_to_sql.exe" '
            r'"C:\Program Files\MySQL\MySQL Server 8.0\share\zoneinfo" | '
            r"mysql -u root -p mysql"
        )
        self.stdout.write("")
        self.stdout.write("Then restart the Django server and reload /admin/.")
