from rest_framework import generics, permissions
from .models import Message, Group
from .serializers import MessageSerializer, GroupSerializer

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        partner_id = self.request.query_params.get('partner')
        return Message.objects.filter(
            sender=user, receiver_id=partner_id
        ) | Message.objects.filter(
            sender_id=partner_id, receiver=user
        ).order_by('created_at')

class GroupListCreateView(generics.ListCreateAPIView):
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Group.objects.filter(
            members__user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
