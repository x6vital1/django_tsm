import random
import string

from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
    Group as AuthGroup,
    Permission as AuthPermission,
)
from django.db import models
from django.utils import timezone
from utils.models import nb


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('first_name', self.generate_random_word())
        extra_fields.setdefault('last_name', self.generate_random_word())
        extra_fields.setdefault('picture', 'http://localhost:8000/')
        extra_fields.setdefault('telegram_id', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)

    @staticmethod
    def generate_random_word():
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(10))


class CustomUser(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(AuthGroup, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(AuthPermission, related_name='customuser_set', blank=True)

    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, **nb)
    last_name = models.CharField(max_length=255, **nb)
    picture = models.CharField(max_length=255, **nb)
    telegram_id = models.IntegerField(default=0)
    email = models.EmailField(max_length=254, **nb)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if self.is_superuser:
            return self.username
        return f'{self.first_name} {self.last_name}'
