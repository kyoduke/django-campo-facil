import os
from django.db import migrations
from django.contrib.auth import get_user_model


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    def generate_superuser(apps, schema_editor):
        from users.models import User

        DJANGO_SU_EMAIL = os.environ.get("SU_EMAIL")
        DJANGO_SU_PASSWORD = os.environ.get("SU_PASSWORD")

        superuser = User.objects.create_superuser(
            email=DJANGO_SU_EMAIL, password=DJANGO_SU_PASSWORD
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
