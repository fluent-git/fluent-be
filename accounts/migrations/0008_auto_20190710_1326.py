# Generated by Django 2.2.1 on 2019-07-10 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20190710_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talkhistory',
            name='end_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='talkhistory',
            name='start_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]