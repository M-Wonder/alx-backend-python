from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, MessageHistory, Notification


class MessagingSignalTests(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='test123')
        self.receiver = User.objects.create_user(username='bob', password='test123')

    def test_post_save_creates_notification(self):
        """Ensure a Notification is created when a new Message is sent."""
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello, Bob!")
        notification = Notification.objects.filter(message=message, user=self.receiver).first()
        self.assertIsNotNone(notification)

    def test_pre_save_logs_old_message(self):
        """Ensure a MessageHistory entry is created when a Message is edited."""
        message = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Initial")
        message.content = "Edited content"
        message.save()

        history_entry = MessageHistory.objects.filter(message=message).first()
        self.assertIsNotNone(history_entry)
        self.assertEqual(history_entry.old_content, "Initial")
        self.assertTrue(message.edited)
