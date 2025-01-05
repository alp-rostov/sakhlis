# Generated by Django 4.2 on 2024-12-22 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apartment',
            options={'verbose_name': 'Appartment', 'verbose_name_plural': 'Appartments'},
        ),
        migrations.AddField(
            model_name='apartment',
            name='link_location',
            field=models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='Link location'),
        ),
    ]