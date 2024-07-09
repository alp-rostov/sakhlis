# Generated by Django 4.2 on 2024-07-09 19:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_site', '0057_alter_apartment_address_num_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlist',
            name='apartment_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.apartment', verbose_name='Appartment'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.userprofile', verbose_name='Client'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='order_status',
            field=models.CharField(blank=True, choices=[('SND', 'New requests'), ('RCV', 'Request sent to the master'), ('END', 'Request finished')], default='SND', max_length=3, null=True, verbose_name='Order status'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='repairer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Repairer'),
        ),
    ]
