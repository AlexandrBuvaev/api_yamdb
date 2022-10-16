from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategorieViewSet, CommentViewSet, GenreViewSet,
                    GetTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UserViewSet)

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename="users")
v1_router.register(r'genres', GenreViewSet, basename="genres")
v1_router.register(r'categories', CategorieViewSet, basename="categories")
v1_router.register(r'titles', TitleViewSet, basename="titles")
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                   r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView),
    path('v1/auth/token/', GetTokenView),
]
