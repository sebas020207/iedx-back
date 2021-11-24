from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


# Create your models here.
class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class Administrator(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.BooleanField(default=False)
    phone = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(null=True, blank=True, upload_to='users/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name


class Info(models.Model):
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=255)
    notice = models.CharField(max_length=255)
    linkedin = models.CharField(max_length=255)

    def __str__(self):
        return self.address
