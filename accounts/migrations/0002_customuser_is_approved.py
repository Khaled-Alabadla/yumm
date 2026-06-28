# Generated manually for owner approval workflow

from django.db import migrations, models


def approve_existing_owners(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.filter(role="owner").update(is_approved=True)
    CustomUser.objects.exclude(role="owner").update(is_approved=True)


def unapprove_all(apps, schema_editor):
    CustomUser = apps.get_model("accounts", "CustomUser")
    CustomUser.objects.filter(role="owner").update(is_approved=False)


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="is_approved",
            field=models.BooleanField(
                db_index=True,
                default=False,
                help_text=(
                    "Restaurant owners must be approved by an admin before they "
                    "can operate on the platform."
                ),
                verbose_name="approved",
            ),
        ),
        migrations.RunPython(approve_existing_owners, unapprove_all),
    ]
