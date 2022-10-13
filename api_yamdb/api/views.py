import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination


from api.serializers import GenreSerializer, CategorieSerializer
from api.serializers import TitleSerializer
from api.permissions import (
    IsReadOnly, IsAuthorOrReadOnly, IsModerOrReadOnly, IsAdminOrReadOnly)

from users.models import User
from titles.models import Genre, Categorie, Title
from reviews.models import Review
from .serializers import (
    GetTokenSerializer, SignUpSerializator, CommentSerializer,
    ReviewSerializer)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет Title (Произведения)."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [
        permissions.IsAdminUser,
        IsReadOnly
    ]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        permissions.IsAdminUser,
        IsReadOnly
    ]


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет категорий."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [
        permissions.IsAdminUser,
        IsReadOnly
    ]


class ReviewViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Review."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrReadOnly,
                          IsAdminOrReadOnly, IsModerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'create':
            permission = permissions.IsAuthenticated
            return [permission()]

        return super().get_permissions()

    def get_queryset(self):
        """Получение списка отзывов к конкретному произведению."""
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.review.all()


class CommentViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        """Получение конкретного объекта модели."""
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def get_permissions(self):
        if self.action == 'create':
            permission = permissions.IsAuthenticated
            return [permission()]

        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['POST'])
def SignUpView(request):
    serializer = SignUpSerializator(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    username = serializer.data.get('username')
    confirmation_code = uuid.uuid4()
    User.objects.get_or_create(
        username=username, email=email, confirmation_code=confirmation_code
    )
    send_mail(
        'Confirmation code from yamdb',
        str(confirmation_code),
        'yamdb<admin@yamdb.ru>', [email]
    )
    return Response('Код успешно отправлен', status=status.HTTP_200_OK)


@api_view(['POST'])
def GetTokenView(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(
        User, username=username, confirmation_code=confirmation_code
    )
    token = RefreshToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)
