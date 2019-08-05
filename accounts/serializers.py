from rest_framework import serializers
from django.contrib.auth.models import User
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


class OpenTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenTime
        fields = ('start', 'end')


class QueueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Queue
        fields = ('id', 'user', 'peerjs_id', 'topic')


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
        fields = ('id', 'username', 'email')


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ('user', 'name', 'rating')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'user', 'clarity', 'pacing',
                  'pronunciation', 'note', 'talk_id')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('id', 'user', 'reason', 'note', 'talk_id')


class TalkHistorySerializer(serializers.ModelSerializer):
    duration = serializers.SerializerMethodField()

    class Meta:
        model = TalkHistory
        fields = ('topic', 'start_time', 'end_time', 'duration', 'id')

    def get_duration(self, obj):
        return obj.get_duration()


class ConversationStarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConversationStarter
        fields = ('id', 'text', 'topic')


class TopicSerializer(serializers.ModelSerializer):
    conversation_starters = ConversationStarterSerializer(
        source='convstarter_topic', many=True)

    class Meta:
        model = Topic
        fields = ('id', 'name', 'is_open', 'conversation_starters')


class TalkDetailSerializer(serializers.ModelSerializer):
    talk_id = TalkHistorySerializer()

    class Meta:
        model = Review
        fields = ('clarity', 'pacing',
                  'pronunciation', 'note', 'talk_id')


class TipsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tips
        fields = ('id', 'text')
