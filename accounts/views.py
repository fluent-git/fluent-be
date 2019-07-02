from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from fluent.settings import CHAT_MAKING_QUEUE

from accounts.serializers import (
    ProfileSerializer,
    UserSerializer,
    RegisterSerializer,
    ReportSerializer,
    ReviewSerializer,
)

from accounts.models import (
    Profile,
    Review,
    Report
)


class FindChatViewSet(generics.CreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        topic = request.data['topic']
        user = User.objects.get(id=request.data['id'])
        user_profile = Profile.objects.get(user=user)
        # user_profile = Profile.objects.get(user=request.user) // use this when using authorization token

        for user in CHAT_MAKING_QUEUE:
            if user['topic'] == topic and user['level'] == user_profile.level:
                CHAT_MAKING_QUEUE.remove(user)
                return Response({'message': 'Found partner to chat', 'id': user['user_id']})

        CHAT_MAKING_QUEUE.append({
            "user_id": user_profile.user.id,
            "topic": topic,
            "level": user_profile.level
        })

        return Response({'message': 'OK'})


class CancelFindChatViewSet(generics.CreateAPIView):
    # permission_classes = (permissions.IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        # user_id = request.user.id // user this when using authorization token
        user_id = request.data['id']
        
        for user in CHAT_MAKING_QUEUE:
            if user['user_id'] == user_id:
                CHAT_MAKING_QUEUE.remove(user)
                break


        return Response({'message': 'OK'})


class ProfileViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()
    

class LoginViewSet(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if not user:
            return Response({'message': 'Invalid username or password'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'OK', 'token': str(token), 'user': UserSerializer(user).data})


class LogoutViewSet(viewsets.GenericViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        token, _ = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response({'message': 'OK'})


class ReviewViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class ReportViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
