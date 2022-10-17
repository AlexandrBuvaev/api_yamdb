import uuid


from api.permissions import (IsAdmin, IsAdminOrReadOnly, IsAuthorOrReadOnly,
                             IsModerOrReadOnly, IsAdminOrReadOnlyGet)
from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Review
from titles.models import Categorie, Genre, Title
from users.models import User


from .serializers import (CategorieSerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignUpSerializator,
                          TitleSerializer, UserNotAdminSerializer,
                          UserSerializer)

class TitleViewSet(viewsets.ModelViewSet):
    """API-вюсет Title (Произведения)."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]


class GenreViewSet(viewsets.ModelViewSet):
    """API-вюсет жанров."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [
        IsAdminOrReadOnlyGet,
    ]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ('name', 'slug')


class CategorieViewSet(viewsets.ModelViewSet):
    """API-вюсет категорий."""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [
        IsAdminOrReadOnlyGet,
    ]
    filter_backends = (
        DjangoFilterBackend,
        filters.SearchFilter,
    )
    search_fields = ('name',)

    # def get_by_slug(self, slug):
    #     return Response({
    #         'status': 'Bad Request',
    #         'message': 'Account could not be created with received data'
    #     }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class ReviewViewSet(viewsets.ModelViewSet):
    """Доступ к объектам модели Review."""

    serializer_class = ReviewSerializer

    queryset = Review.objects.all()
    permission_classes = [IsAuthorOrReadOnly
                          , IsAdminOrReadOnly , IsModerOrReadOnly]
    # pagination_class = LimitOffsetPagination

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
    try:
        user, create = User.objects.get_or_create(
            username=username, email=email
        )
    except IntegrityError:
        return Response(
            'Такой логин или email уже существуют',
            status=status.HTTP_400_BAD_REQUEST
        )
    confirmation_code = uuid.uuid4()
    user.confirmation_code = confirmation_code
    user.save()
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
    permission_classes = [IsAuthenticated, IsAdmin]
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        permission_classes=(IsAuthenticated,),
        detail=False,
        url_name='me',
        url_path='me'
    )
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user)
        if request.method == 'GET':
            serializer = UserNotAdminSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = UserNotAdminSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
