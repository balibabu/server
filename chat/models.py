from django.contrib.auth.models import User
from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        users = [self.sender, self.receiver]
        users.sort(key=lambda user: user.id)
        Conversation.objects.update_or_create(
            user1=users[0],
            user2=users[1],
            defaults={'last_message': self}
        )

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='conversations_user2')
    last_message = models.OneToOneField(Message, on_delete=models.SET_NULL, null=True, blank=True)
