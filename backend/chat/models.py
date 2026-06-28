from django.db import models
from django.conf import settings
import uuid

class Group(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)

class GroupMember(models.Model):
    ROLE_CHOICES = [('admin','Admin'),('member','Member')]
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='members'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='member'
    )
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('group', 'user')

class Message(models.Model):
    STATUS_CHOICES = [
        ('sent','Sent'),
        ('delivered','Delivered'),
        ('read','Read')
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='received_messages'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='messages'
    )
    content = models.TextField(blank=True)
    encrypted_blob = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='sent'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)

class ChatMetadata(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_metadata'
    )
    chat_partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='+'
    )
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        null=True, blank=True
    )
    last_seen = models.DateTimeField(null=True, blank=True)
    last_delivered = models.DateTimeField(null=True, blank=True)
    unread_count = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

class PushToken(models.Model):
    PLATFORM_CHOICES = [('android','Android'),('ios','iOS')]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='push_tokens'
    )
    fcm_token = models.TextField()
    platform = models.CharField(
        max_length=10, choices=PLATFORM_CHOICES, default='android'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class MessageDelivery(models.Model):
    STATUS_CHOICES = [
        ('pending','Pending'),
        ('delivered','Delivered'),
        ('failed','Failed')
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE,
        related_name='delivery_attempts'
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending'
    )
    attempt_count = models.IntegerField(default=0)
    last_attempted_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
