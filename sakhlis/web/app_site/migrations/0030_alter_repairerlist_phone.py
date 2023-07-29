# Generated by Django 4.2 on 2023-07-17 19:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0029_alter_orderlist_repairer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairerlist',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')], verbose_name='Телефон'),
        ),
    ]