# Generated by Django 3.2.8 on 2021-10-31 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('mobile_phone', models.CharField(max_length=12)),
                ('phone', models.CharField(max_length=12)),
                ('company', models.CharField(max_length=255)),
                ('area', models.CharField(max_length=255)),
                ('priority', models.CharField(choices=[('l', 'Low'), ('m', 'Medium'), ('h', 'High')], default='l', max_length=1)),
                ('product', models.ManyToManyField(to='products.Product')),
            ],
        ),
    ]
