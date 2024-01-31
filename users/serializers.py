from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class UserBaseSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserAuthSerializer(UserBaseSerializer):
    pass


class UserCreateSerializer(UserBaseSerializer):

    def validate_username(self, username):
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError('User already exists!')
