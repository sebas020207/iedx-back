# Generated by Django 3.2.7 on 2021-11-14 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotes', '0004_quote_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='company',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='mobile_phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='quote',
            name='phone',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
