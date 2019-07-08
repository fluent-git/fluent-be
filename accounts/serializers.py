from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import (
    Profile,
    Review,
    Report
)


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ('user', 'name', 'level')


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
            'email',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'clarity', 'pacing',
                  'pronunciation', 'note', 'talk_id')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'user', 'reason', 'note', 'talk_id')
