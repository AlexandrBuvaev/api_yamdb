from django.urls import path

from .views import GetTokenView, SignUpView

urlpatterns = [
    path('v1/auth/signup/', SignUpView),
    path('v1/auth/token/', GetTokenView)
]
