import rest_framework.permissions
from rest_framework import serializers

from .models import User


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
