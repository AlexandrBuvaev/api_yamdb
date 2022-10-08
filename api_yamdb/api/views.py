from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from review.models import Review
from .serializers import CommentSerializer, ReviewSerializer
from .permissions import (
    IsAuthorOrReadOnly, IsModerOrReadOnly, IsAdminOrReadOnly)

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Post."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthorOrReadOnly
                          | IsAdminOrReadOnly | IsModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        """Получение конкретного объекта модели."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
