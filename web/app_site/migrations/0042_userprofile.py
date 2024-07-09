# Generated by Django 4.2 on 2024-05-03 16:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_site', '0041_alter_repairer_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Name')),
                ('phone', models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{8,15}$')], verbose_name='Phone')),
                ('telegram', models.CharField(blank=True, max_length=25, null=True, verbose_name='Telegram')),
                ('city', models.CharField(choices=[('TB', 'Tbilisi'), ('BT', 'Batumi')], default='TB', max_length=2)),
                ('profile', models.CharField(blank=True, default='', max_length=1500, null=True, verbose_name='About me:')),
                ('foto', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='Photo:')),
                ('rating_sum', models.IntegerField(blank=True, default=0, null=True)),
                ('rating_num', models.IntegerField(blank=True, default=1, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'UserProfile',
                'verbose_name_plural': 'UserProfile',
            },
        ),
    ]