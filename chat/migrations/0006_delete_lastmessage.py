# Generated by Django 5.0 on 2023-12-26 16:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_remove_lastmessage_user1_remove_lastmessage_user2_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='LastMessage',
        ),
    ]
