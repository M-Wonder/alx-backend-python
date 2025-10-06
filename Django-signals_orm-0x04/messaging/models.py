from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --------------------------------------------------------------------
# Custom Manager: Filters unread messages for a given user
# --------------------------------------------------------------------
class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        """
        Return only unread messages for the specified user.
        Uses .only() to optimize query fields retrieved from the DB.
        """
        return (
            self.get_queryset()
            .filter(receiver=user, read=False)
            .only("id", "sender", "receiver", "content", "timestamp")
        )


# --------------------------------------------------------------------
# Message Model: includes read flag, timestamps, and signals integration
# --------------------------------------------------------------------
class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)

    # Default manager
    objects = models.Manager()
    # Custom unread manager
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ["-timestamp"]


# --------------------------------------------------------------------
# MessageHistory Model: stores previous versions of edited messages
# --------------------------------------------------------------------
class MessageHistory(models.Model):
    message = models.ForeignKey(
        Message, related_name="history", on_delete=models.CASCADE
    )
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History of Message ID {self.message.id}"


# --------------------------------------------------------------------
# Notification Model: stores user notifications triggered by signals
# --------------------------------------------------------------------
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}"
