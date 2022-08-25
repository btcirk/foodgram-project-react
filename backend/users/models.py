from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ADMIN = 'admin'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'admin'),
        (USER, 'user'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    role = models.CharField('Роль пользователя',
                            max_length=5,
                            choices=ROLE_CHOICES,
                            default=USER)
    confirmation_code = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.username
