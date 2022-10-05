from rest_framework import serializers
from users.models import User


class UserEmailRegistration(serializers.ModelSerializer):
    """Класс сериализатор для 'email'."""
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)


class UserConfirmation(serializers.Serializer):
    """Класс сериализатор для подтверждения 'email'."""
    pass


class UserSerializer(serializers.ModelSerializer):
    """Класс сериализатор для 'User'."""
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'bio', 'role', 'email'
        )
