# Generated by Django 4.2.14 on 2024-08-09 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_fields', '0008_alter_footballfield_hour_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='footballfield',
            name='main_image',
            field=models.ImageField(blank=True, null=True, upload_to='football_fields_images'),
        ),
        migrations.AlterField(
            model_name='address',
            name='football_field',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='football_fields.footballfield'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='football_field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='football_fields.footballfield'),
        ),
    ]
