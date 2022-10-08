from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GenreViewSet, CategorieViewSet, TitleViewSet, GetTokenView, SignUpView

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'genres', GenreViewSet, basename="genres")
v1_router.register(r'categories', CategorieViewSet, basename="categories")
v1_router.register(r'titles', TitleViewSet, basename="titles")

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', SignUpView),
    path('v1/auth/token/', GetTokenView),
    ]