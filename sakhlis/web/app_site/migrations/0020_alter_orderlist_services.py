# Generated by Django 4.2 on 2023-05-13 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0019_remove_invoice_date_in_alter_orderlist_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='services',
            field=models.ManyToManyField(blank=True, null=True, through='app_site.Invoice', to='app_site.service'),
        ),
    ]
