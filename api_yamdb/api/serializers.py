from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.db.models import Avg

from review.models import Comment, Review

User = get_user_model()


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
        score = self.context['request'].score
        if score < 1 and score > 10:
            raise serializers.ValidationError(
                'Оценка произведений от 1 до 10.')

    def get_rating(self, obj):
        rating = Review.objects.filter(
            title=obj.title).aggregate(Avg('score'))
        return rating
