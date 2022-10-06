import datetime

from rest_framework import serializers
from titles.models import Genre, Categorie, Title


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
