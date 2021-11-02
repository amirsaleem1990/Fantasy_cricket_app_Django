from django.db import models

from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    email      = models.CharField(max_length=100)
    full_name  = models.CharField(max_length=100)
    password   = models.CharField(max_length=100)
    username   = models.CharField(max_length=100)
    