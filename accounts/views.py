from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import mixins, viewsets

from accounts.serializers import (
    UserSerializer,
)

class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
