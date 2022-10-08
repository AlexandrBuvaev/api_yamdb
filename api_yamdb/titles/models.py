import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


MIN_VALUE_YEAR = 1900


def current_year():
    """Вернуть текущий год."""
    return datetime.date.today().year


def max_value_current_year(value):
    """Вернуть максимальное значение года для валидатора."""
    return MaxValueValidator(current_year())(value)


class Genre(models.Model):
    """
    Класс модели Genre (Жанры).

    содержит Field:
    name - Жанр
    slug - Адрес
    """

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        """Вернуть жанр (name)."""
        return self.name


class Categorie(models.Model):
    """
    Класс модели Categories (Категории).

    содержит Field:
    name - Категория
    slug - Адрес
    """

    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """Вернуть категорию (name)."""
        return self.name


class Title(models.Model):
    """
    Класс модели Title (Произведения).

    содержит Field:
    name - Название
    year - Год выпуска
    description - Описание
    genre - Ссылка на модель Genre (Жанр) ManyToMany
    category- Ссылка на модель Сategory (Категорию)
    """

    name = models.TextField(
        'Название',
        help_text='Название произведения',
    )
    year = models.PositiveIntegerField(
        'Год выпуска',
        default=datetime.datetime.now().year,
        validators=[
            max_value_current_year,
            MinValueValidator(MIN_VALUE_YEAR)
        ]
    )
    description = models.SlugField(unique=True)
    genre = models.ManyToManyField(
        Genre,
        related_name='genres',
        verbose_name='Жанр',
        help_text='Жанр произведения',
    )
    category = models.ForeignKey(
        Categorie,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='categories',
        verbose_name='Категория',
        help_text='Категория произведения',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        """Вернуть Произведение"""
        return self.name
