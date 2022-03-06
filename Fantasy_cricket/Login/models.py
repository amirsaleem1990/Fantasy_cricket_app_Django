from django.db import models
from django.contrib.auth.models import User

from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    # full_name field is not exist in default django user table, so we add it here
    full_name = models.CharField(max_length=100)