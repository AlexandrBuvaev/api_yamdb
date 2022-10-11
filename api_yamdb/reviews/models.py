from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title
from users.models import User


class Review(models.Model):
    """Класс отзыва. Основные поля:
    author - автор отзыва,
    score - рейтинг от 0-10,
    text - текст отзыва,
    title - прозведение,
    average_score - ср.значение рейтинга."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviewer',
        null=False,
        blank=False
    )
    score = models.DecimalField(
        max_digits=2,
        decimal_places=0,
        validators=[
            MaxValueValidator(10), MinValueValidator(1)],
        null=False,
        blank=False
    )
    text = models.TextField(
        null=False,
        blank=False
    )
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
        null=False,
        blank=False
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментария. Связывает произведение, автора и текст."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='commentator',
        null=False,
        blank=False
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        null=False,
        blank=False
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True,
        null=False,
        blank=False
    )
