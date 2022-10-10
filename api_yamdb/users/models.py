from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USERS_ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ')
]


class User(AbstractUser):
    email = models.EmailField(_('email_address'), unique=True)
    bio = models.TextField(max_length=250, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(
        max_length=25, choices=USERS_ROLES,
        default='user'
    )

    def is_admin(self):
        self.role == 'admin' or self.is_staff

    def is_moderator(self):
        self.role == 'moderator'
