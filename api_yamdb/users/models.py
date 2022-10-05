from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Виды пользовательских ролей.
CHOICES = [
    ('admin', 'Администратор'),
    ('moderator', 'Модератор'),
    ('user', 'Пользователь'),
]


class User(AbstractUser):
    """
    Кастомный класс пользователя.
    Переопределено поле "email",
    Добавлены поля 'bio', 'confirmation_code', 'role'.
    Добавлены методы для проверки ролей пользователя,
    по умолчанию стоит пользователь.
    """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    confirmation_code = models.CharField(max_length=60, blank=True)
    role = models.CharField(max_length=30, choices=CHOICES, default='user')

    def is_moderator(self):
        """Метод возвращает True, если пользователь является модератором."""
        return self.role == 'moderator'

    def is_admin(self):
        """
        Метод возвращает True, если пользователь являеться администратором.
        """
        return self.role == 'admin' or self.is_staff
