import uuid

from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly,
                             IsModerOrReadOnly, IsReadOnly)
from api.serializers import (CategorieSerializer, GenreSerializer,
                             TitleSerializer)
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review
from titles.models import Categorie, Genre, Title
from users.models import User

from .serializers import (CommentSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializator,
                          UserNotAdminSerializer, UserSerializer)


class TitleViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет Title (Произведения)."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [
        IsAdminUser,
        IsReadOnly
    ]


class GenreViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminUser,
        IsReadOnly
    ]


class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    """API-вюсет категорий."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [
        IsAdminUser,
        IsReadOnly
    ]


class ReviewViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Post."""

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsAuthorOrReadOnly
                          | IsAdminOrReadOnly | IsModerOrReadOnly]
    # pagination_class = LimitOffsetPagination

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
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def GetTokenView(request):
    serializer = GetTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if user.confirmation_code == confirmation_code:
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [IsAdminUser | IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', ]

    @action(
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated],
        detail=False,
        url_name='me',
        url_path='me'
    )
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        if self.request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(user,
                                            data=request.data,
                                            partial=True)
            else:
                serializer = UserNotAdminSerializer(user,
                                                    data=request.data,
                                                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
