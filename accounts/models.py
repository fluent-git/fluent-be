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


class Report(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='report')
    reason = models.CharField(max_length=100, blank=False)
    note = models.TextField(default='', blank=True)


class Review(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='review')
    clarity = models.IntegerField(default=0)
    pacing = models.IntegerField(default=0)
    pronunciation = models.IntegerField(default=0)
    note = models.TextField(default='', blank=True)
