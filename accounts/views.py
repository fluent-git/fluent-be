from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
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
    Report,
    TalkHistory,
)


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


class ProfileViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class QueueViewSet(viewsets.GenericViewSet):
    # TODO adjust with peerjs server
    # permission_classes = (permissions.IsAuthenticated,)
    
    @action(methods=['post'], detail=False)
    def start(self, request):
        topic = request.data['topic']
        user = User.objects.get(id=request.data['user_id'])
        user_profile = Profile.objects.get(user=user)
        # user_profile = Profile.objects.get(user=request.user) // use this when using authorization token

        for queue in CHAT_MAKING_QUEUE:
            if queue['topic'] == topic and queue['level'] == user_profile.level:
                CHAT_MAKING_QUEUE.remove(queue)
                return Response({
                    'message': 'Found partner to chat',
                    'user_id': queue['user_id'],
                    'peerjs_id': queue['peerjs_id'],
                    'conversation_suggestion': ""
                })
    
        CHAT_MAKING_QUEUE.append({
            "user_id": user_profile.user.id,
            "topic": topic,
            "level": user_profile.level,
            "peerjs_id": request.data['peerjs_id']
        })

        return Response({'message': 'Queuing'})

    @action(methods=['post'], detail=False)
    def cancel(self, request):
        # user_id = request.user.id // user this when using authorization token
        user_id = request.data['user_id']
        
        for user in CHAT_MAKING_QUEUE:
            if user['user_id'] == user_id:
                CHAT_MAKING_QUEUE.remove(user)
                break

        return Response({'message': 'OK'})
    
    @action(methods=['post'], detail=False)
    def check(self, request):
        return Response({'message': 'OK'})


class ReportViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Report.objects.all()
    serializer_class = ReportSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class TalkViewSet(viewsets.GenericViewSet):
    # TODO define serializer and model

    @action(methods=['post'], detail=False)
    def start(self, request):
        user1 = User.objects.get(id=request.data['user1_id'])
        user2 = User.objects.get(id=request.data['user2_id'])

        talk_history = TalkHistory.objects.create(
            user1=user1,
            user2=user2,
            topic=request.data['topic']
        )
        talk_history.save()
        print(talktalk_history_History.id)

        return Response({'message': 'OK', 'talk_id': talk_History.id})
    
    @action(methods=['post'], detail=False)
    def end(self, request):
        talk_history = TalkHistory.objects.get(id=request.data['talk_id'])
        talk_history.end_time = datetime.now()
        talk_history.save()

        return Response({'message': 'OK'})

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()
