# Generated by Django 3.2.8 on 2021-11-01 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20211031_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='provider',
            name='address',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='provider',
            name='phone',
            field=models.CharField(max_length=12),
        ),
    ]
