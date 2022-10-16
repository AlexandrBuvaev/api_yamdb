import datetime

from django.db.models import Avg

from rest_framework import serializers

from reviews.models import Comment, Review
from titles.models import Categorie, Genre, Title
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
        many=True, slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Categorie.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_year(self, value):
        """Валидация года."""
        if value > datetime.date.today().year:
            raise serializers.ValidationError("Not valid")
        return value


class TitleViewSerializer(serializers.ModelSerializer):
    category = CategorieSerializer(read_only=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')
        read_only_fields = ('id', 'name', 'year', 'rating',
                            'description', 'genre', 'category')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
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
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        fields = '__all__'
        model = Review
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title'],
                message='Пользователь уже писал рецензию на произведение!')
        ]

    def validate_score(self, data):
        """Проверка оценки произведения на вхождение в диапазон от 1 до 10. """
        score = self.initial_data.get('score')
        if int(score) > 0 and int(score) < 11:
            raise serializers.ValidationError(
                'Оценка произведений от 1 до 10.')
        return data

    def get_rating(self, obj):
        """Вычисление среднего рейтинга произведения."""
        rating = Review.objects.filter(
            title=obj.title).annotate(Avg('score'))
        return rating


class SignUpSerializator(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        if attrs['username'] == 'me':
            raise serializers.ValidationError('Нельзя использовать логин "me"')
        return attrs

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    confirmation_code = serializers.CharField(max_length=60, required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class UserNotAdminSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
