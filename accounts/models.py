from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    clarity = models.IntegerField(default=0)
    pacing = models.IntegerField(default=0)
    pronunciation = models.IntegerField(default=0)
    note = models.TextField(default='', blank=True)


class Report(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='report')
    reason = models.CharField(max_length=100, blank=False)
    note = models.TextField(default='', blank=True)
