# Generated by Django 3.2.7 on 2021-11-05 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('historical', '0003_rename_date_history_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='action',
            field=models.TextField(),
        ),
    ]
