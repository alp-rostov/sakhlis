# Generated by Django 4.2 on 2023-04-17 17:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0007_alter_order_address_city_id_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='City',
            new_name='CityDirectory',
        ),
        migrations.RenameModel(
            old_name='Order',
            new_name='OrderList',
        ),
        migrations.RenameModel(
            old_name='Repairer',
            new_name='RepairerList',
        ),
    ]