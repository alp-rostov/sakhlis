# Generated by Django 4.2 on 2024-04-22 18:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0049_rename_streertbilisi_streettbilisi_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientfeedback',
            name='order_id',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.orderlist', verbose_name='Order'),
        ),
    ]
