from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Avg

User = get_user_model()


class Review(models.Model):
    """Класс отзыва. Основные поля:
    author - автор отзыва,
    score - рейтинг от 0-10,
    text - текст отзыва,
    title - прозведение,
    average_score - ср.значение рейтинга."""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviewer'
        )
    score = models.DecimalField(
        max_digits=10, decimal_places=0
        )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True
        )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='review'
        )

    # def average_score(self):
    #     average_score = Review.objects.filter(title=title).aggregate(Avg('score'))
    #     return average_score

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментария. Связывает произведение, автора и текст."""

    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='commentator'
    )
    review = models.ForeignKey(
        Review, on_delete=models.SET_NULL, related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
