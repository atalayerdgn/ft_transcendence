from rest_framework import serializers
from src.models.models import User
from django.contrib.auth import authenticate

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password'
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'created_at',
            'updated_at',
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TwoFASerializer(serializers.Serializer):
    twofa_code = serializers.CharField(required=True)

    
class UpdateUserSerializer(serializers.Serializer):
    current_username = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def validate_email(self, value):
        # validated_data üzerinden current_username alınır
        current_username = self.initial_data.get('current_username')  # Bu kısım değiştirildi
        if User.objects.filter(email=value).exclude(username=current_username).exists():
            raise serializers.ValidationError("Email already in use.")
        return value
