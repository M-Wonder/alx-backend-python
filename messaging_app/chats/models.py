
#!/usr/bin/env python3
"""
Models for messaging application:
- Custom User model extending AbstractUser
- Conversation model to group participants
- Message model for storing messages
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    """
    Custom User model extending AbstractUser.
    Adds UUID primary key, phone_number, and role.
    """
    USER_ROLES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]

    user_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='guest')
    created_at = models.DateTimeField(default=timezone.now)

    # Remove username uniqueness (use email instead for login)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Conversation model representing a chat between multiple users.
    """
    conversation_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Message model representing an individual message in a conversation.
    """
    message_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        db_index=True
    )
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="messages_sent"
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Message from {self.sender.email} at {self.sent_at}"
