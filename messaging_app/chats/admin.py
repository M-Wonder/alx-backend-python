from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Conversation, Message


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'role')}),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Conversation admin"""
    list_display = ['conversation_id', 'created_at', 'participant_count']
    list_filter = ['created_at']
    search_fields = ['conversation_id']
    filter_horizontal = ['participants']
    
    def participant_count(self, obj):
        return obj.participants.count()
    participant_count.short_description = 'Participants'


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Message admin"""
    list_display = ['message_id', 'sender', 'conversation', 'sent_at', 'message_preview']
    list_filter = ['sent_at']
    search_fields = ['message_body', 'sender__email']
    readonly_fields = ['message_id', 'sent_at']
    
    def message_preview(self, obj):
        return obj.message_body[:50] + '...' if len(obj.message_body) > 50 else obj.message_body
    message_preview.short_description = 'Preview'
