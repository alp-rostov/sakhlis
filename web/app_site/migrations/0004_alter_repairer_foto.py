# Generated by Django 4.2 on 2023-04-15 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_site', '0003_alter_repairer_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repairer',
            name='foto',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
