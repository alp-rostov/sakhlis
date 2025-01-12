# Generated by Django 4.2 on 2024-12-20 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('app_site', '0062_remove_clientfeedback_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartment',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.userprofile', verbose_name='Responsible person for apartment'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clients.userprofile', verbose_name='Client'),
        ),
        migrations.DeleteModel(
            name='ClientFeedback',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
