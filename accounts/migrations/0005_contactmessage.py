# Generated manually for ContactMessage model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_merge_20260628_2013"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="full name")),
                (
                    "email",
                    models.EmailField(max_length=254, verbose_name="email address"),
                ),
                (
                    "subject",
                    models.CharField(
                        choices=[
                            ("Restaurant Partnership", "Restaurant Partnership"),
                            ("Technical Support", "Technical Support"),
                            ("Media & Press", "Media & Press"),
                            ("General Inquiry", "General Inquiry"),
                        ],
                        db_index=True,
                        max_length=50,
                        verbose_name="subject",
                    ),
                ),
                ("message", models.TextField(max_length=1000, verbose_name="message")),
                (
                    "is_read",
                    models.BooleanField(
                        db_index=True,
                        default=False,
                        help_text="Mark when the message has been reviewed.",
                        verbose_name="read",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="received at"
                    ),
                ),
            ],
            options={
                "verbose_name": "contact message",
                "verbose_name_plural": "contact messages",
                "ordering": ["-created_at"],
            },
        ),
    ]
