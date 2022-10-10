from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Класс отзыва. Основные поля:
    author - автор отзыва,
    score - рейтинг от 0-10,
    text - текст отзыва,
    title - прозведение,
    average_score - ср.значение рейтинга."""

    list_display = (
        # 'pk',
        'author',
        'score',
        'text',
        'pub_date',
        'title',
    )
    list_editable = ('text',)
    search_fields = ('text',)
    empty_value_display = '-пусто-'
