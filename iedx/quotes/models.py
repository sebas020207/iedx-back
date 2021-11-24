from django.db import models

from products.models import Product
# Create your models here.


class Quote(models.Model):
    LOW = 'L'
    MEDIUM = 'M'
    HIGH = 'H'
    PRIORITY_TYPES = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    mobile_phone = models.CharField(max_length=12, blank=True, null=True)
    phone = models.CharField(max_length=12, blank=True, null=True)
    company = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_TYPES, default=LOW)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    product = models.ManyToManyField(Product)

    def __str__(self):
        return 'Priority: '+self.priority

    def email_message(self):
        message = 'Cliente: '
        message += self.last_name + ' '+self.first_name+'\n'
        message += 'Email: ' + self.email+'\n'
        message += 'Dirección: ' + self.address+'\n'
        message += 'Teléfono fijo: ' + self.phone+'\n'
        message += 'Teléfono móvil: ' + self.mobile_phone+'\n'
        message += 'Compañía: ' + self.company+'\n'
        message += 'Area: ' + self.area+'\n'
        message += 'Prioridad: ' + self.priority+'\n'
        message += 'Productos: '
        for product in self.product.all():
            message += product.name+', '
        return message


class Registry(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)
    messagereg = models.CharField(max_length=255, blank=True, null=True)

    def email_message_registry(self):
        message = 'Cliente: '
        message += self.name+'\n'
        message += 'Email: ' + self.email+'\n'
        message += 'Dirección: ' + self.address+'\n'
        message += 'Teléfono: ' + self.phone+'\n'
        message += 'Asunto: ' + self.subject+'\n'
        message += 'Mensaje: ' + self.messagereg+'\n'
        return message
