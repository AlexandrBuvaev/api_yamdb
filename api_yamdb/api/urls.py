from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategorieViewSet, TitleViewSet

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'genre', GenreViewSet, basename="genres")
v1_router.register(r'categorie', CategorieViewSet, basename="categories")
v1_router.register(r'titles', TitleViewSet, basename="titles")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
