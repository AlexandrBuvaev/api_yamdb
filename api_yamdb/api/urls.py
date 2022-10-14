from django.urls import include, path
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import GenreViewSet, CategorieViewSet, TitleViewSet, GetTokenView, SignUpView, ReviewViewSet, CommentViewSet
=======
from .views import (CommentViewSet, GenreViewSet, CategorieViewSet,
                    GetTokenView, ReviewViewSet, SignUpView, TitleViewSet,
                    UserViewSet)
>>>>>>> 685de7723df4e0ee82884088addfdb42b450a03e

app_name = 'api'

v1_router = DefaultRouter()
v1_router.register(r'users', UserViewSet, basename="users")
v1_router.register(r'genres', GenreViewSet, basename="genres")
v1_router.register(r'categories', CategorieViewSet, basename="categories")
v1_router.register(r'titles', TitleViewSet, basename="titles")
<<<<<<< HEAD
v1_router.register(r'titles/(?P<title_id>)/reviews/(?P<review_id>)/comments',
                   ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                   CommentViewSet, basename='comments')
=======
v1_router.register(
    r'titles/(?P<title_id>)/reviews/(?P<review_id>)/comments',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    CommentViewSet, basename='comments'
)
>>>>>>> 685de7723df4e0ee82884088addfdb42b450a03e

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', SignUpView),
    path('v1/auth/token/', GetTokenView),
]
