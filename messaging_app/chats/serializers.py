from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'password', 'first_name', 
                  'last_name', 'phone_number', 'role', 'created_at']
        read_only_fields = ['user_id', 'created_at']
    
    def validate_email(self, value):
        """Validate email uniqueness"""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
    
    def create(self, validated_data):
        """Create user with hashed password"""
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model"""
    sender = UserSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    sender_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'sender_id', 'sender_email', 
                  'conversation', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def get_sender_email(self, obj):
        """Get sender's email address"""
        return obj.sender.email if obj.sender else None
    
    def validate_message_body(self, value):
        """Validate message body is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def create(self, validated_data):
        """Create a new message"""
        sender_id = validated_data.pop('sender_id')
        try:
            sender = User.objects.get(user_id=sender_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sender does not exist.")
        
        message = Message.objects.create(sender=sender, **validated_data)
        return message


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model with nested messages"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'participant_ids', 
                  'messages', 'message_count', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def get_message_count(self, obj):
        """Get total number of messages in conversation"""
        return obj.messages.count()
    
    def validate_participant_ids(self, value):
        """Validate that at least 2 participants are provided"""
        if value and len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value
    
    def create(self, validated_data):
        """Create a new conversation with participants"""
        participant_ids = validated_data.pop('participant_ids', [])
        conversation = Conversation.objects.create()
        
        if participant_ids:
            participants = User.objects.filter(user_id__in=participant_ids)
            if participants.count() != len(participant_ids):
                raise serializers.ValidationError("One or more participants do not exist.")
            conversation.participants.set(participants)
        
        return conversation
