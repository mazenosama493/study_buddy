from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer
from notes.models import Note
from users.models import CustomUser

# List and create notifications
class NotificationListCreateView(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Retrieve only notifications for the logged-in user."""
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')

    
    def perform_create(self, serializer):
        notification_type = self.request.data.get('notification_type')
        note = self.request.data.get('note')

        # Require note for specific notification types
        if notification_type in ['like', 'dislike', 'comment', 'new_note']:
            if not note:
                raise serializers.ValidationError(
                    {"error": f"A 'note' must be provided for notification type '{notification_type}'."}
                )
        note = None
        if note:
            try:
                note = Note.objects.get(id=note_id)
            except Note.DoesNotExist:
                raise serializers.ValidationError({"error": "Note not found."})

    
        message = ""
        if notification_type == "like":
            message = f"{self.request.user.username} liked your note."
        elif notification_type == "dislike":
            message = f"{self.request.user.username} disliked your note."
        elif notification_type == "comment":
            message = f"{self.request.user.username} commented on your note."
        elif notification_type == "follow":
            message = f"{self.request.user.username} started following you."
        elif notification_type == "new_note":
            message = f"{self.request.user.username} published a new note."
        elif notification_type == "follow_accepted":
            message = f"{self.request.user.username} accepted your follow request."
        elif notification_type == "follow_rejected":
            message = f"{self.request.user.username} rejected your follow request."
        else:
            message = f"{self.request.user.username} sent you a notification."

        serializer.save(sender=self.request.user, message=message)

# Retrieve, update (mark as seen), and delete a notification
class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    def perform_update(self, serializer):
        """Mark notification as seen on update."""
        serializer.save(seen=True)
