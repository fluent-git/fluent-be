from datetime import datetime

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField("auth.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=True)
    level = models.IntegerField(null=True)

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def __str__(self):
        return self.user.username + ' ' + self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class TalkHistory(models.Model):
    user1 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_history1')
    user2 = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='talk_history2')
    topic = models.TextField(default='', blank=True)
    start_time = models.DateTimeField(default=datetime.now(), blank=True)
    end_time = models.DateTimeField(default=datetime.now(), blank=True)

    def get_talk_time(self):
        return self.end_time - self.start_time


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
