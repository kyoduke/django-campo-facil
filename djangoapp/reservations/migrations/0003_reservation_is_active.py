# Generated by Django 4.2.15 on 2024-09-20 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
