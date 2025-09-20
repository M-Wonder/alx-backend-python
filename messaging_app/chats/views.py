#!/usr/bin/env python3
"""
ViewSets for Conversations and Messages in the messaging app.
Provides API endpoints to list, create, and interact with conversations.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating conversations.
    Includes a custom action to add participants.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expects a list of user_ids as participants.
        """
        participant_ids = request.data.get("participants", [])
        participants = User.objects.filter(user_id__in=participant_ids)

        if not participants:
            return Response(
                {"error": "At least one valid participant is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        """
        Custom endpoint to add a participant to an existing conversation.
        """
        conversation = self.get_object()
        user_id = request.data.get("user_id")
        user = get_object_or_404(User, user_id=user_id)
        conversation.participants.add(user)
        conversation.save()
        return Response({"status": "participant added"})


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating messages.
    Supports sending messages to an existing conversation.
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        """
        Send a new message to a conversation.
        Expects sender_id, conversation_id, and message_body.
        """
        sender_id = request.data.get("sender_id")
        conversation_id = request.data.get("conversation_id")
        message_body = request.data.get("message_body")

        sender = get_object_or_404(User, user_id=sender_id)
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        message = Message.objects.create(
            sender=sender,
            conversation=conversation,
            message_body=message_body,
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
