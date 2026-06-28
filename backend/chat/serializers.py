from rest_framework import serializers
from .models import Message, Group

class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(
        source='sender.username', read_only=True
    )
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_username',
            'receiver', 'group', 'content',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'sender', 'status', 'created_at']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at']
