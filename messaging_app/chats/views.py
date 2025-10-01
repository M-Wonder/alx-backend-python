#!/usr/bin/env python3
"""
Views for conversations and messages in the messaging_app.
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation


class ConversationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for conversations.
    Only authenticated participants can access their conversations.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    # Global IsAuthenticated + Custom IsParticipantOfConversation
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Restrict conversations to only those where the user is a participant.
        """
        user = self.request.user
        return Conversation.objects.filter(participants=user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for messages.
    Only authenticated participants of the conversation can access messages.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]

    def get_queryset(self):
        """
        Restrict messages to only those in conversations
        where the user is a participant.
        """
        user = self.request.user
        return Message.objects.filter(conversation__participants=user)
