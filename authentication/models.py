import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models

# Create your models here.


# class User(AbstractUser):
#     USERNAME_FIELD = 'email'


class TemporaryRegisteredUsers(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.CharField(max_length=100, unique=True)
    date_created = models.DateTimeField(auto_now=True)
