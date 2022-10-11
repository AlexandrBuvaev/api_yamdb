from unicodedata import category
from django.contrib import admin

from .models import Genre, Categorie, Title


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """
    Класс админки Categorie (Категории).

    содержит Field:
    name - Категория
    slug - Адрес
    """

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenresAdmin(admin.ModelAdmin):
    """
    Класс админки Genres (Жанры).

    содержит Field:
    name - Жанр
    slug - Адрес
    """

    list_display = (
        'pk',
        'name',
        'slug',
    )
    list_editable = ('slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """
    Класс админки Title (Произведения).

    содержит Field:
    name - Название
    year - Год выпуска
    description - Описание
    genre - Ссылка на модель Genre (Жанр)
    category- Ссылка на модель Сategory (Категорию)
    """

    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'get_genre',
        'category',
    )
    list_editable = ('category',)
    search_fields = ('name',)
    list_filter = ('year',)
    empty_value_display = '-пусто-'

    def get_genre(self, obj):
        """Вывод жанров"""
        return "\n".join([g.name for g in obj.genre.all()])
