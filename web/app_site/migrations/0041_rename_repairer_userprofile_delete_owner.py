# Generated by Django 4.2 on 2024-03-31 18:11

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_site', '0040_alter_invoice_options_alter_orderlist_options_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Repairer',
            new_name='UserProfile',
        ),
        migrations.DeleteModel(
            name='Owner',
        ),
    ]
