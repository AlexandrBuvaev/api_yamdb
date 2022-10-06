from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentsViewSet

router = DefaultRouter()

router.register(r'/titles/(?P<title_id>)/reviews/(?P<review_id>)/comments',
                ReviewViewSet, basename='reviews')
router.register(r'/titles/(?P<title_id>\d+)/reviews',
                CommentsViewSet, basename='comments')

app_name = 'api'

urlpatterns = [
    path('v1/', include(router.urls)),
]

