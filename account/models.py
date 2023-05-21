from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from .manager import UserProfileManager


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='user', blank=True, null=True)
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=60, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()



    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_prem(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

