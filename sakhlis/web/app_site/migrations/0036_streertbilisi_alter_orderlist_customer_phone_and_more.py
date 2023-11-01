# Generated by Django 4.2 on 2023-11-01 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0035_alter_repairerlist_foto'),
    ]

    operations = [
        migrations.CreateModel(
            name='StreerTbilisi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_street', models.CharField(max_length=50)),
                ('name_street', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_phone',
            field=models.CharField(max_length=16, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='orderlist',
            name='customer_telegram',
            field=models.CharField(blank=True, max_length=26, null=True, verbose_name='Telegram'),
        ),
    ]
