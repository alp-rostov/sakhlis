# Generated by Django 4.2 on 2024-12-26 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0002_alter_apartment_options_apartment_link_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='address_num',
            field=models.CharField(blank=True, default=' ', max_length=150, null=True, verbose_name='Apartment (number, entrance, floor etc.)'),
        ),
    ]
