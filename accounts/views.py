from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import mixins, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from accounts.serializers import (
    UserSerializer,
    ReviewSerializer,
    ReportSerializer
)

from accounts.models import (
    Review,
    Report
)


class UserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if not user:
            return Response({'message': 'Invalid username or password'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': str(token), 'user': UserSerializer(user).data})


class LogoutViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        token, _ = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response({'message': 'OK'})


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReportViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
