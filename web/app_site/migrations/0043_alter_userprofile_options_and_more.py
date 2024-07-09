# Generated by Django 4.2 on 2024-04-08 19:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0042_apartment_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': 'UserProfile', 'verbose_name_plural': 'UserProfile'},
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='apartment_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='app_site.apartment', verbose_name='Appartment'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo:'),
        ),
    ]