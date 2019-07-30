from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

User._meta.get_field('email')._unique = True


class OpenTime(models.Model):
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=24)


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True)
    rating = models.IntegerField(default=0)

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def __str__(self):
        return self.user.username + ' ' + self.user.email


class TalkHistory(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_history1')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_history2')
    topic = models.TextField(default='', blank=True)
    start_time = models.DateTimeField(default=timezone.now, blank=True)
    end_time = models.DateTimeField(default=timezone.now, blank=True)
    active = models.BooleanField(default=True)

    def get_duration(self):
        return int((self.end_time - self.start_time).total_seconds())


class Report(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='report')
    reason = models.CharField(max_length=100, blank=False)
    note = models.TextField(default='', blank=True)
    talk_id = models.ForeignKey(
        TalkHistory, on_delete=models.CASCADE, related_name='report_talk_id', default=None)


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    clarity = models.IntegerField(default=0)
    pacing = models.IntegerField(default=0)
    pronunciation = models.IntegerField(default=0)
    note = models.TextField(default='', blank=True)
    talk_id = models.ForeignKey(
        TalkHistory, on_delete=models.CASCADE, related_name='review_talk_id', default=None)


class Queue(models.Model):
    user = models.IntegerField(default=0, unique=True)
    peerjs_id = models.TextField(default='')
    topic = models.TextField(default='')


class Topic(models.Model):
    name = models.CharField(max_length=24, blank=False)
    is_open = models.BooleanField(default=True)


class ConversationStarter(models.Model):
    text = models.CharField(max_length=100, default='')
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name='convstarter_topic', default=None)
