from django.db import models
from django.utils import timezone


class Stock(models.Model):
    date = models.DateTimeField(default=timezone.now)
    stock_code = models.CharField(max_length=10, unique=True)
    stock_name = models.CharField(max_length=50)
    price = models.FloatField()
    change = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    capacity = models.FloatField()

    
from django.db import models

class ETF_list(models.Model):
    etf_code = models.CharField(max_length=10, unique=True)
    etf_name = models.CharField(max_length=50)
    price = models.FloatField(blank=True, null=True)
    change = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"{self.etf_code} - {self.etf_name}"
    

class PopularStock(models.Model):
    stock_code = models.CharField(max_length=10, unique=True)
    stock_name = models.CharField(max_length=50)
    price = models.FloatField()
    change = models.FloatField()
    high = models.FloatField()
    open = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    capacity = models.FloatField()

# class Data(models.Model):
#     date = models.DateTimeField(default=timezone.now)

from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin

class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    cBirthday = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=16)
    id = models.BigAutoField(primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    