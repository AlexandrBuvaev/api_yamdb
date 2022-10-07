import uuid

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User

from .serializers import GetTokenSerializer, SignUpSerializator


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
