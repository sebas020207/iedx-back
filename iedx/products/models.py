from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=255)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField(null=True, blank=True, upload_to='products/')

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_archived = models.BooleanField(default=False)
    photo = models.ImageField(null=True, blank=True, upload_to='products/')
    supplier_id = models.ForeignKey(
        Supplier, blank=True, null=True, on_delete=models.SET_NULL)
    category_id = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL)
    subcategory_id = models.ForeignKey(
        Subcategory, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
