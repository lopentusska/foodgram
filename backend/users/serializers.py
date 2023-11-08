from django.contrib.auth.models import update_last_login
from django.shortcuts import get_object_or_404
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken

from follows.models import Follow
from .models import User


class UserSerializer(UserSerializer, serializers.ModelSerializer):
    """Serializer for user model."""
    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            self.fields['is_subscribed'] = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
        )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Follow.objects.filter(user=user, following=obj).exists()


class RegisterSerializer(UserSerializer):
    """Custom register serializer."""
    password = serializers.CharField(
        max_length=150,
        min_length=8,
        write_only=True,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainSerializer):
    """Custom login serializer."""
    email = serializers.EmailField(
        max_length=150,
        write_only=True,
        required=True)
    password = serializers.CharField(
        max_length=150,
        min_length=8,
        write_only=True,
        required=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            raise AuthenticationFailed('Invalid credentials')

        data = super().validate(attrs)
        access = AccessToken.for_user(user)

        data['user'] = UserSerializer(self.user).data
        data['access'] = str(access)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
