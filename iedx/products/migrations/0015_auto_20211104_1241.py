# Generated by Django 3.2.7 on 2021-11-04 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20211104_1118'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='id_category',
            new_name='category_id',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='id_subcategory',
            new_name='subcategory_id',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='id_supplier',
            new_name='supplier_id',
        ),
    ]
