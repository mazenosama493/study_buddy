from django.db import models
from django.conf import settings

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('follow_request', 'Follow Request'),
        ('follow_accepted', 'Follow Accepted'),
        ('follow_rejected', 'Follow Rejected'),
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('comment', 'Comment'),
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.ForeignKey('notes.Note', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.sender} -> {self.recipient} ({self.notification_type})"
