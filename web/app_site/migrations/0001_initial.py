# Generated by Django 4.2 on 2023-04-15 16:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Repairer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('s_name', models.CharField(max_length=100, null=True)),
                ('phone', models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')])),
                ('email', models.EmailField(max_length=200, null=True)),
                ('foto', models.ImageField(height_field=200, null=True, upload_to='static/images', width_field=200)),
                ('active', models.BooleanField(default=False)),
                ('rating_sum', models.IntegerField(default=0)),
                ('rating_num', models.IntegerField(default=0)),
                ('city_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_site.city')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_in', models.DateTimeField(auto_now_add=True)),
                ('time_out', models.DateTimeField(null=True)),
                ('price', models.IntegerField(max_length=5, null=True)),
                ('text_order', models.CharField(max_length=1500)),
                ('customer_name', models.CharField(max_length=50)),
                ('customer_phone', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')])),
                ('customer_feedback', models.CharField(max_length=1500, null=True)),
                ('address_street_app', models.CharField(max_length=150)),
                ('address_city_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_site.city')),
                ('repairer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_site.repairer')),
            ],
        ),
    ]
