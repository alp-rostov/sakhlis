# Generated by Django 4.2 on 2023-10-01 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0031_alter_invoice_options_alter_orderlist_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='repairerlist',
            name='telegram',
            field=models.CharField(blank=True, max_length=25, null=True, unique=True, verbose_name='Телеграм'),
        ),
    ]
