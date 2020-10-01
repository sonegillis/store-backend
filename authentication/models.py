import random
import string
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


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='profile')
    referral_code = models.CharField(max_length=100, unique=True)
    points = models.IntegerField()

    def get_random_string(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(6))

    def __str__(self):
        return "{}".format(self.user.username)

    def save(self, *args, **kwargs):
        self.referral_code = self.get_random_string()
        return super(UserProfile, self).save()
