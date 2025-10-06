from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message

@cache_page(60)  # Cache for 60 seconds
@login_required
def conversation_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation).order_by('-timestamp')
    return render(request, 'chats/conversation_messages.html', {'messages': messages})
