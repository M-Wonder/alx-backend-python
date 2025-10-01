#!/usr/bin/env python3
"""
Custom permissions for messaging_app.
"""

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users
    - Only participants in a conversation can view, send, update or delete messages
    """

    def has_permission(self, request, view):
        # ✅ Only authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is a participant:
        - For Conversation: user must be in participants
        - For Message: user must be in conversation participants
        """
        if hasattr(obj, "participants"):  # Conversation object
            return request.user in obj.participants.all()

        if hasattr(obj, "conversation"):  # Message object
            return request.user in obj.conversation.participants.all()

        return False
