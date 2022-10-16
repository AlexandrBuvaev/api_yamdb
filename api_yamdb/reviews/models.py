from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from titles.models import Title
from users.models import User


class Review(models.Model):
    """Класс отзыва. Основные поля:
    author - автор отзыва,
    score - рейтинг от 1-10,
    text - текст отзыва,
    title - прозведение"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review'
            )
        ]
    
    
    def __str__(self):
        return self.text


class Comment(models.Model):
    """Класс комментария. Связывает произведение, автора и текст."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField()

    def __str__(self):
        return self.author

   
     
