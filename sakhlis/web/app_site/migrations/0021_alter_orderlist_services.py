# Generated by Django 4.2 on 2023-05-13 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0020_alter_orderlist_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='services',
            field=models.ManyToManyField(through='app_site.Invoice', to='app_site.service'),
        ),
    ]