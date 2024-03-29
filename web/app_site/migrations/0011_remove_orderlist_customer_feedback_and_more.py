# Generated by Django 4.2 on 2023-05-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0010_orderlist_address_area_orderlist_address_num_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='customer_feedback',
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='address_area',
            field=models.CharField(choices=[('--', 'Район'), ('DB', 'Дидубе'), ('KR', 'Крцаниси'), ('ND', 'Надзаладеви'), ('GR', 'Грмагеле'), ('ZG', 'Згвис'), ('GL', 'Глдани'), ('DI', 'Дигоми'), ('DD', 'Диди Дигоми'), ('IS', 'Исани'), ('SM', 'Самгори')], default='', max_length=3, null=True, verbose_name='Район'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_phone',
            field=models.CharField(max_length=16, verbose_name='Номер телефона'),
        ),
    ]
