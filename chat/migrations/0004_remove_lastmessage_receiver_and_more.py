# Generated by Django 5.0 on 2023-12-26 14:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_lastmessage_delete_conversation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastmessage',
            name='receiver',
        ),
        migrations.RemoveField(
            model_name='lastmessage',
            name='sender',
        ),
        migrations.AddField(
            model_name='lastmessage',
            name='user1',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='last_messages_user1', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lastmessage',
            name='user2',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='last_messages_user2', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]