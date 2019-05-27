from rest_framework import serializers
from django.contrib.auth.models import User
from accounts.models import (
    Review,
    Report
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'clarity', 'pacing', 'pronunciation', 'note')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'user', 'reason', 'note')
