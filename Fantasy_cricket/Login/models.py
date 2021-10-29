from django.db import models

from django.contrib.auth.models import User

# class ExtendedUser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     email      = models.CharField(max_length=100)
#     first_name = models.CharField(max_length=100)
#     last_name  = models.CharField(max_length=100)
#     password   = models.CharField(max_length=100)


from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    email      = models.CharField(max_length=100)
    full_name  = models.CharField(max_length=100)
    password   = models.CharField(max_length=100)
    username   = models.CharField(max_length=100)
    