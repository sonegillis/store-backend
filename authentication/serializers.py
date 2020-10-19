from django.contrib.auth.models import User
from rest_framework import serializers

from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        excludes = ('user',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'profile', 'is_superuser', 'username', 'first_name', 'last_name', 'email', 'is_staff',
                  'is_active')
