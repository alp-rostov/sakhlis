# Generated by Django 4.2 on 2024-12-26 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0003_alter_apartment_address_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apartment',
            name='notes',
        ),
    ]
