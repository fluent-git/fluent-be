# Generated by Django 2.2.1 on 2019-07-07 17:37

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalkHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.TextField(blank=True, default='')),
                ('start_time', models.DateTimeField(blank=True, default=datetime.datetime(2019, 7, 8, 0, 37, 27, 350030))),
                ('end_time', models.DateTimeField(blank=True, default=datetime.datetime(2019, 7, 8, 0, 37, 27, 350050))),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_history1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='talk_history2', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
