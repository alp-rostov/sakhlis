# Generated by Django 4.2 on 2023-04-25 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0008_rename_city_citydirectory_rename_order_orderlist_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='address_city_id',
        ),
        migrations.RemoveField(
            model_name='repairerlist',
            name='city_id',
        ),
        migrations.AddField(
            model_name='orderlist',
            name='address_city',
            field=models.CharField(choices=[('TB', 'Тбилиси'), ('BT', 'Батуми'), ('RS', 'Рустави')], default='TB', max_length=2),
        ),
        migrations.AddField(
            model_name='repairerlist',
            name='city',
            field=models.CharField(choices=[('TB', 'Тбилиси'), ('BT', 'Батуми'), ('RS', 'Рустави')], default='TB', max_length=2),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_feedback',
            field=models.CharField(max_length=2500, null=True),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7, null=True),
        ),
        migrations.DeleteModel(
            name='CityDirectory',
        ),
    ]
