from .models import Notification

def send_notification(sender, recipient, notification_type, message):
    """ Creates a new notification """
    Notification.objects.create(
        sender=sender,
        recipient=recipient,
        notification_type=notification_type,
        message=message
    )
