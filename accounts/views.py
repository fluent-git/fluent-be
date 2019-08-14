import random
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.analyze import analyze

from fluent.settings import CHAT_MAKING_QUEUE

from accounts.serializers import (
    ConversationStarterSerializer,
    ProfileSerializer,
    QueueSerializer,
    RegisterSerializer,
    ReportSerializer,
    ReviewSerializer,
    TalkHistorySerializer,
    UserSerializer,
    OpenTimeSerializer,
    TalkDetailSerializer,
    TopicSerializer,
    TipsSerializer
)

from accounts.models import (
    Profile,
    Queue,
    Review,
    Report,
    TalkHistory,
    OpenTime,
    Topic,
    ConversationStarter,
    Tips
)


class RegisterView(viewsets.GenericViewSet):

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        if not self.valid(request.data):
            return Response({'message': 'Email or Username already exist'})

        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )

        profile = Profile.objects.create(
            user=user,
            rating=request.data['level']*1000
        )
        profile.save()

        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    def valid(self, user_data):
        user_from_email = User.objects.filter(email=user_data['email'])
        user_from_username = User.objects.filter(
            username=user_data['username'])

        return len(user_from_email) == 0 and len(user_from_username) == 0


class Analyze(APIView):
    def post(self, request, format='json'):
        input = request.data['input_text']
        source = request.data['source_text']
        time = request.data['input_time']
        expected_time = request.data['expected_time'] if 'expected_time' in request.data else 0

        return Response(analyze(input, source, time, expected_time))


class LoginView(viewsets.GenericViewSet):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        user = authenticate(
            username=request.data['username'], password=request.data['password'])
        if not user:
            return Response({'message': 'Invalid username or password'})

        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'OK', 'token': str(token), 'user': UserSerializer(user).data})


class LogoutView(viewsets.GenericViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        token, _ = Token.objects.get_or_create(user=request.user)
        token.delete()
        return Response({'message': 'OK'})


class OpenTimeViewSet(viewsets.ModelViewSet):
    # permission_classes = (permissions.IsAuthenticated,)
    queryset = OpenTime.objects.all()
    serializer_class = OpenTimeSerializer

    def patch(self, request, pk=1):
        opentime = OpenTime.objects.get(pk=pk)
        opentime.start = request.data['start']
        opentime.end = request.data['end']
        opentime.save()
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
        ).order_by('-start_time')

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
    queryset = Queue.objects.all()

    @transaction.atomic
    @action(methods=['post'], detail=False)
    def start(self, request):
        topic = request.data['topic']
        user1 = User.objects.get(id=request.data['user_id'])
        user_profile = Profile.objects.get(user=user1)
        queues = Queue.objects.filter(topic=topic)
        # user_profile = Profile.objects.get(user=request.user) // use this when using authorization token

        if len(queues) > 0:
            for queue in queues:
                if queue.user == user_profile.id:
                    continue

                '''
                TODO refactor this code below
                Function should not have complex bussiness logic
                '''
                user2 = User.objects.get(id=queue.user)
                talk = TalkHistory.objects.create(
                    user1=user1, user2=user2, topic=topic
                )
                queue.delete()

                return Response({
                    'message': 'Found partner to chat',
                    'user_id': queue.user,
                    'peerjs_id': queue.peerjs_id,
                    'talk_id': talk.id
                })
        else:
            queue = Queue.objects.create(
                user=user_profile.user.id,
                topic=topic,
                peerjs_id=request.data['peerjs_id']
            )

        return Response({'message': 'Queuing'})

    @action(methods=['post'], detail=False)
    def cancel(self, request):
        queues = Queue.objects.all()
        # user_id = request.user.id // user this when using authorization token
        user_id = request.data['user_id']

        for queue in queues:
            if queue.user == user_id:
                queue.delete()
                break

        return Response({'message': 'OK'})

    @action(methods=['post'], detail=False)
    def check(self, request):
        opentime = OpenTime.objects.get(pk=1)
        start = opentime.start
        end = opentime.end
        now = timezone.now().hour
        topic_name = request.data['topic']
        topic = TopicSerializer(Topic.objects.get(name=topic_name)).data

        if not topic['is_open']:
            message = 'ERR_TOPIC'
        elif now >= start and now < end:
            message = 'OK'
        else:
            message = 'ERR_TIME'

        return Response({
            'message': message,
            'start': start,
            'end': end
        })

    @action(methods=['get'], detail=False)
    def print(self, request):
        queues = Queue.objects.all()
        return Response(QueueSerializer(queues, many=True).data)

    @action(methods=['post'], detail=False)
    def reset(self, request):
        queues = Queue.objects.all()

        for queue in queues:
            queue.delete()

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
        talk_history = get_object_or_404(
            TalkHistory, id=request.data['talk_id'])
        talk_history.end_time = timezone.now()
        talk_history.active = False
        talk_history.save()

        return Response({'message': 'OK'})

    @action(methods=['post'], detail=False)
    def recent_talk(self, request):
        talk_history = TalkHistory.objects.filter(
            Q(user1=request.data['user_id']) | Q(user2=request.data['user_id'])
        ).order_by('-start_time')

        return Response(TalkHistorySerializer(talk_history, many=True).data)

    @action(methods=['post'], detail=False)
    def talk_detail(self, request):
        review = get_object_or_404(
            Review,
            user=request.data['user_id'],
            talk_id=request.data['talk_id']
        )

        return Response(TalkDetailSerializer(review).data)


class TopicViewSet(viewsets.GenericViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def create(self, request):
        name = request.data['name']
        is_open = request.data['is_open']
        topic = Topic.objects.create(
            name=name,
            is_open=is_open
        )
        topic.save()

        return Response(TopicSerializer(topic).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        results = self.get_queryset()
        topics = []
        for topic in results:
            topics.append({
                'id': topic.id,
                'topic': topic.name,
                'is_open': topic.is_open
            })

        return Response({'results': topics})

    @action(methods=['post'], detail=False)
    def details(self, request):
        topic_name = request.data['topic']
        topic = TopicSerializer(Topic.objects.get(name=topic_name)).data
        conversation_starters = [conversation_starter['text']
                                 for conversation_starter in topic['conversation_starters']]
        random.shuffle(conversation_starters)
        topic['conversation_starters'] = conversation_starters

        tipsobjects = Tips.objects.all()
        tips = [TipsSerializer(tipsobject).data['text']
                for tipsobject in tipsobjects]
        random.shuffle(tips)
        topic['tips'] = tips

        return Response(topic)

    # TODO : Fix URLS to be able to get pk (pk not yet defined)
    def patch(self, request, pk):
        topic = Topic.objects.get(pk=pk)
        if 'name' in request.data:
            topic.name = request.data['name']
        if 'is_open' in request.data:
            topic.name = request.data['is_open']
        topic.save()

        return Response({'message': 'OK'})

    @action(methods=['post'], detail=False)
    def open(self, request):
        topic_name = request.data['topic']
        topic = Topic.objects.get(name=topic_name)
        topic.is_open = True
        topic.save()
        return Response({'message': 'OK'})

    @action(methods=['post'], detail=False)
    def close(self, request):
        topic_name = request.data['topic']
        topic = Topic.objects.get(name=topic_name)
        topic.is_open = False
        topic.save()
        return Response({'message': 'OK'})


class ConversationStarterViewSet(viewsets.ModelViewSet):
    queryset = ConversationStarter.objects.all()
    serializer_class = ConversationStarterSerializer

    def create(self, request):
        topic = get_object_or_404(Topic, name=request.data['topic']).id
        # try:
        #     topic = Topic.objects.get(name=request.data['topic']).id
        # except ObjectDoesNotExist:
        #     return Response("Invalid Topic", status=status.HTTP_404_NOT_FOUND)
        request.data['topic'] = topic

        return super().create(request)

    def patch(self, request, pk):
        conversation_starter = ConversationStarter.objects.get(pk=pk)
        conversation_starter.text = request.data['text']
        conversation_starter.save()

        return Response({'message': 'OK'})


class TipsViewSet(viewsets.ModelViewSet):
    queryset = Tips.objects.all()
    serializer_class = TipsSerializer
