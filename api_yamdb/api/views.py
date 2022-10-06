from rest_framework import viewsets, permissions

from api.serializers import GenreSerializer, CategorieSerializer
from api.serializers import TitleSerializer
from api.permissions import IsReadOnly
from titles.models import Genre, Categorie, Title


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
