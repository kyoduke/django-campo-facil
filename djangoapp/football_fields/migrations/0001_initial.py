# Generated by Django 4.2.15 on 2024-09-09 13:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FootballField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='football_fields_images')),
                ('name', models.CharField(default='Campo', max_length=100)),
                ('field_dimensions', models.CharField(blank=True, default='', max_length=9)),
                ('description', models.TextField(blank=True, default='', max_length=1500)),
                ('grass_type', models.CharField(choices=[('SIN', 'Sintético'), ('NAT', 'Natural'), ('HIB', 'Híbrido')], default='SIN', max_length=3)),
                ('has_field_lighting', models.BooleanField(blank=True, default=False)),
                ('has_changing_room', models.BooleanField(blank=True, default=False)),
                ('hour_price', models.PositiveSmallIntegerField(null=True)),
                ('facilities', models.TextField(blank=True, default='', max_length=500)),
                ('rules', models.TextField(blank=True, default='', max_length=1500)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='football_fields_images')),
                ('football_field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='football_fields.footballfield')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_one', models.CharField(max_length=300)),
                ('address_two', models.CharField(blank=True, max_length=300)),
                ('state', models.CharField(choices=[('RJ', 'Rio de Janeiro'), ('SP', 'São Paulo'), ('MG', 'Minas Gerais')], default='', max_length=2)),
                ('city', models.CharField(max_length=200)),
                ('district', models.CharField(max_length=50)),
                ('cep_code', models.CharField(max_length=9)),
                ('latitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=7, max_digits=9, null=True)),
                ('football_field', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='football_fields.footballfield')),
            ],
        ),
    ]
