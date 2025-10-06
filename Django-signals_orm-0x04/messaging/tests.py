from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class DeleteUserSignalTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='alice', password='1234')
        self.user2 = User.objects.create_user(username='bob', password='1234')

        self.msg = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hi Bob!")
        self.msg.content = "Hi Bob! (edited)"
        self.msg.save()  # triggers MessageHistory

    def test_user_deletion_cleans_related_data(self):
        """Ensure messages, notifications, and histories are deleted when user is removed."""
        self.user1.delete()

        self.assertFalse(Message.objects.exists())
        self.assertFalse(Notification.objects.exists())
        self.assertFalse(MessageHistory.objects.exists())
