from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)  # ✅ track if message was edited

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"


class MessageHistory(models.Model):
    """
    Stores old versions of messages before being edited.
    Automatically created by the pre_save signal.
    """
    message = models.ForeignKey(Message, related_name='history', on_delete=models.CASCADE)
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Edit history for Message ID {self.message.id} at {self.edited_at}"


class Notification(models.Model):
    """
    Created automatically via the post_save signal when a new message is sent.
    """
    user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.ForeignKey(Message, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username} about Message ID {self.message.id}"
