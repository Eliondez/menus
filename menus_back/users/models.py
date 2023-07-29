from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    restaurant = models.ForeignKey(
        'menu.Restaurant',
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name='users',
    )