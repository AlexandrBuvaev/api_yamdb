from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERS_ROLES = [
        ('user', 'Пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Админ')]

    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=250, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(
        max_length=25, choices=USERS_ROLES,
        default='user'
    )

    @property
    def is_admin(self):
        return (
            self.role == 'admin'
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return (
            self.role == 'moderator'
            or self.is_superuser
        )
