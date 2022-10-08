import datetime

from django.db.models import Avg
from rest_framework import serializers
from review.models import Comment, Review
from titles.models import Genre, Categorie, Title
from users.models import User


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор Genre (Жанры)."""

    class Meta:
        model = Genre
        fields = '__all__'


class CategorieSerializer(serializers.ModelSerializer):
    """Сериализатор Categorie (категории)."""

    class Meta:
        model = Categorie
        fields = '__all__'


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор Title (Произведения)."""
    genre = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='name'
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Categorie.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        """Валидация года."""
        if value['not_valid']:
            raise serializers.ValidationError("Not valid")
        if self.year > datetime.date.today().year:
            raise serializers.ValidationError("Not valid")
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Пользователь уже писал рецензию на произведение!')
        ]

    def validate_score(self):
        """Проверка оценки произведения на вхождение в диапазон от 1 до 10. """
        score = self.context['request'].score
        if score < 1 and score > 10:
            raise serializers.ValidationError(
                'Оценка произведений от 1 до 10.')

    def get_rating(self, obj):
        """Вычисление среднего рейтинга произведения."""
        rating = Review.objects.filter(
            title=obj.title).aggregate(Avg('score'))
        return rating


class SignUpSerializator(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    confirmation_code = serializers.CharField(max_length=60, required=True)
