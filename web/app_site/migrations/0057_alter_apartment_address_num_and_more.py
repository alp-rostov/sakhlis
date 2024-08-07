# Generated by Django 4.2 on 2024-07-09 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0056_alter_userprofile_phone_alter_userprofile_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='address_num',
            field=models.CharField(blank=True, default=' ', max_length=10, null=True, verbose_name='House number'),
        ),
        migrations.AlterField(
            model_name='apartment',
            name='address_street_app',
            field=models.CharField(blank=True, default=' ', max_length=150, null=True, verbose_name='Street'),
        ),
    ]
