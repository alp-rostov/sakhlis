# Generated by Django 4.2 on 2023-10-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0033_repairerlist_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairerlist',
            name='foto',
            field=models.ImageField(blank=True, height_field=800, null=True, upload_to='images/', verbose_name='Фотография:', width_field=800),
        ),
    ]
