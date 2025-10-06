from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification

class MessageSignalTest(TestCase):
    def setUp(self):
        self.sender = User.objects.create_user(username='alice', password='123')
        self.receiver = User.objects.create_user(username='bob', password='123')

    def test_notification_created_on_message(self):
        msg = Message.objects.create(sender=self.sender, receiver=self.receiver, content="Hello Bob!")
        notification = Notification.objects.filter(user=self.receiver, message=msg).exists()
        self.assertTrue(notification, "Notification should be created when a message is sent")
