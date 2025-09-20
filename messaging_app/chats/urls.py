
#!/usr/bin/env python3
"""
URL configuration for the messaging_app project.
Routes for Conversations and Messages APIs are registered here.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chats.views import ConversationViewSet, MessageViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # API endpoints for conversations and messages
]
