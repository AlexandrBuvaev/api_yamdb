from rest_framework import serializers
from users.models import User


class SignUpSerializator(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30, required=True)
    confirmation_code = serializers.CharField(max_length=60, required=True)
