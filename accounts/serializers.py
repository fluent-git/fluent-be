from rest_framework import serializers
from django.contrib.auth.models import User
# from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')
