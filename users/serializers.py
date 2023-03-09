import os
from datetime import datetime, timedelta

import jwt
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from users.models import CustomUser

JWT_SECRET = os.environ.get('SECRET_KEY')
JWT_ACCESS_TTL = 60 * 5
JWT_REFRESH_TTL = 3600 * 24 * 7


class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('email',)

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('email',)

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = CustomUser
        fields = ('is_active', 'is_staff', 'role', 'email', 'first_name', 'last_name')

class CustomRegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True,)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password': self.validated_data.get('password', ''),
            'username': self.validated_data.get('username', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
        }

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            username = validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate email and password
        email = validated_data['email']
        password = validated_data['password']
        error_msg = _('email or password are incorrect')
        try:
            user = CustomUser.objects.get(email=email)
            if not user.check_password(password):
                raise serializers.ValidationError(error_msg)
            validated_data['user'] = user
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['user'].id,
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {
            'access': access,
            'refresh': refresh
        }


class RefreshSerializer(serializers.Serializer):
    # ==== INPUT ====
    refresh_token = serializers.CharField(required=True, write_only=True)
    # ==== OUTPUT ====
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        # standard validation
        validated_data = super().validate(attrs)

        # validate refresh
        refresh_token = validated_data['refresh_token']
        # print(refresh_token)
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=['HS256'])
            if payload['type'] != 'refresh':
                error_msg = {'refresh_token': _('Token type is not refresh!')}
                raise serializers.ValidationError(error_msg)
            validated_data['payload'] = payload
        except jwt.ExpiredSignatureError:
            error_msg = {'refresh_token': _('Refresh token is expired!')}
            raise serializers.ValidationError(error_msg)
        except jwt.InvalidTokenError:
            error_msg = {'refresh_token': _('Refresh token is invad!')}
            raise serializers.ValidationError(error_msg)

        return validated_data

    def create(self, validated_data):
        access_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['payload']['user_id'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_ACCESS_TTL),
            'type': 'access'
        }
        access = jwt.encode(payload=access_payload, key=JWT_SECRET)

        refresh_payload = {
            'iss': 'backend-api',
            'user_id': validated_data['payload']['user_id'],
            'exp': datetime.utcnow() + timedelta(seconds=JWT_REFRESH_TTL),
            'type': 'refresh'
        }
        refresh = jwt.encode(payload=refresh_payload, key=JWT_SECRET)

        return {
            'access': access,
            'refresh': refresh
        }