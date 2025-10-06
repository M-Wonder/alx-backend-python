from django.contrib import admin
from .models import Message, MessageHistory, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'edited')
    search_fields = ('sender__username', 'receiver__username', 'content')
    list_filter = ('edited', 'timestamp')


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_at', 'old_content')
    search_fields = ('message__sender__username', 'old_content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
