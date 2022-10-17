import datetime

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

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        default=serializers.CurrentUserDefault(),
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('title',)

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = (
                self.context['request'].parser_context['kwargs']['title_id']
            )
            user = self.context['request'].user
            if Review.objects.filter(author=user, title_id=title_id).exists():
                raise serializers.ValidationError(
                    'Нельзя оставить отзыв на прозведение дважды.'
                )
        return data


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
