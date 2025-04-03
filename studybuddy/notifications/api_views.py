from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer

# List and create notifications
class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve only notifications for the logged-in user."""
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# Retrieve, update (mark as seen), and delete a notification
class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        """Mark notification as seen on update."""
        serializer.save(seen=True)
