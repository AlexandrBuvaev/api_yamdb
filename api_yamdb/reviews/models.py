from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(models.Model):
    """Класс отзыва. Основные поля:
    author - автор отзыва,
    score - рейтинг от 0-10,
    text - текст отзыва,
    title - прозведение,
    average_score - ср.значение рейтинга."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='author')
    score = models.DecimalField(max_digits=10, decimal_places=0)
    text = models.TextField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
