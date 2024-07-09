# Generated by Django 4.2 on 2024-04-12 16:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_site', '0043_alter_userprofile_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlist',
            name='customer_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.userprofile', verbose_name='Client'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='customer_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='apartment_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.apartment', verbose_name='Appartment'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='repairer_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Repairer'),
        ),
    ]