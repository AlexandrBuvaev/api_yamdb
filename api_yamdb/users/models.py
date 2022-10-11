from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

USERS_ROLES = [
    ('USER', 'Пользователь'),
    ('MODERATOR', 'Модератор'),
    ('ADMIN', 'Админ')
]


class User(AbstractUser):
    email = models.EmailField(_('email_address'), unique=True)
    bio = models.TextField(max_length=250, blank=True)
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(
        max_length=25, choices=USERS_ROLES,
        default='USER'
    )

    @property
    def is_user(self):
        self.role == 'USER'

    @property
    def is_admin(self):
        self.role == 'ADMIN' or self.is_staff

    @property
    def is_moderator(self):
        self.role == 'MODERATOR'
