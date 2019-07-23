from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.analyze import analyze

from fluent.settings import CHAT_MAKING_QUEUE

from accounts.serializers import (
    ProfileSerializer,
    RegisterSerializer,
    ReportSerializer,
    ReviewSerializer,
    TalkHistorySerializer,
    UserSerializer,
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

    @action(methods=['post'], detail=False)
    def summary(self, request):
        talk_history = TalkHistory.objects.filter(
            Q(user1=request.data['user_id']) | Q(
                user2=request.data['user_id']),
            active=False
        )

        reviews = Review.objects.filter(user=request.data['user_id'])

        if len(reviews) == 0:
            return Response({
                'talk_count': len(talk_history),
                'reviews': 'No reviews yet'
            })
        else:
            clarity = pacing = pronunciation = 0
            for review in reviews:
                clarity += review.clarity
                pacing += review.pacing
                pronunciation += review.pronunciation

            return Response({
                'talk_count': len(talk_history),
                'clarity': clarity / len(reviews),
                'pacing': pacing / len(reviews),
                'pronunciation': pronunciation / len(reviews)
            })


class QueueViewSet(viewsets.GenericViewSet):
    # TODO adjust with peerjs server
    # permission_classes = (permissions.IsAuthenticated,)

    @action(methods=['post'], detail=False)
    def start(self, request):
        topic = request.data['topic']
        user1 = User.objects.get(id=request.data['user_id'])
        user_profile = Profile.objects.get(user=user1)
        # user_profile = Profile.objects.get(user=request.user) // use this when using authorization token

        for queue in CHAT_MAKING_QUEUE:
            if queue['user_id'] == user_profile.id:
                CHAT_MAKING_QUEUE.remove(queue)
            elif queue['topic'] == topic and queue['level'] == user_profile.level:
                CHAT_MAKING_QUEUE.remove(queue)

                '''
                TODO refactor this code below
                Function should not have complex bussiness logic
                '''
                user2 = User.objects.get(id=queue['user_id'])
                talk = TalkHistory.objects.create(
                    user1=user1, user2=user2, topic=topic)

                return Response({
                    'message': 'Found partner to chat',
                    'user_id': queue['user_id'],
                    'peerjs_id': queue['peerjs_id'],
                    'conversation_suggestion': "",
                    'talk_id': talk.id
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

    @action(methods=['get'], detail=False)
    def print(self, request):
        return Response({'queue': CHAT_MAKING_QUEUE})

    @action(methods=['post'], detail=False)
    def reset(self, request):
        CHAT_MAKING_QUEUE = []
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
        user = request.data['user_id']

        '''
        TODO refactor this code below
        TalkHistory that has user2=user and active=True should not be more than one
        '''
        talk_history = TalkHistory.objects.filter(
            user2=user, active=True).latest('id')

        return Response({
            'message': 'OK',
            'user_id': talk_history.user1.id,
            'talk_id': talk_history.id,
            'conversation_suggestion': ""
        })

    @action(methods=['post'], detail=False)
    def end(self, request):
        talk_history = TalkHistory.objects.get(id=request.data['talk_id'])
        talk_history.end_time = timezone.now()
        talk_history.active = False
        talk_history.save()

        return Response({'message': 'OK'})

    @action(methods=['post'], detail=False)
    def recent_talk(self, request):
        talk_history = TalkHistory.objects.filter(
            Q(user1=request.data['user_id']) | Q(user2=request.data['user_id'])
        )

        return Response(TalkHistorySerializer(talk_history, many=True).data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = (AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)

        return super(UserViewSet, self).get_permissions()


class Analyze(APIView):
    def post(self, request, format='json'):
        input = request.data['input_text']
        source = request.data['source_text']
        time = request.data['input_time']
        expected_time = request.data['expected_time'] if 'expected_time' in request.data else 0
        return Response(analyze(input, source, time, expected_time))
