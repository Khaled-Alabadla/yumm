# Generated manually for city and address on CustomUser

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_merge_20260628_1437"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="address",
            field=models.CharField(blank=True, max_length=500, verbose_name="address"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="city",
            field=models.CharField(
                blank=True, db_index=True, max_length=30, verbose_name="city"
            ),
        ),
    ]
