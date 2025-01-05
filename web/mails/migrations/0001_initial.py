# Generated by Django 4.2 on 2024-12-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mail', models.EmailField(blank=True, max_length=254, null=True)),
                ('flag', models.BooleanField(default=False)),
            ],
        ),
    ]