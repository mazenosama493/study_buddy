from notifications.models import Notification
from profile_users.models import Follow  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')

    for notification in notifications:
        if notification.notification_type == 'follow_request':
            follow_request = Follow.objects.filter(
                follower=notification.sender, 
                following=request.user, 
                status='pending'
            ).first()
            notification.follow_request_id = follow_request.id if follow_request else None

    return render(request, 'notifications/notifications.html', {'notifications': notifications})

@login_required
def mark_notifications_as_seen(request):
    """ Marks all notifications as seen for the logged-in user """
    Notification.objects.filter(recipient=request.user, seen=False).update(seen=True) 
    return redirect('notifications')
@login_required
def mark_single_notification_as_seen(request, notification_id):
    """ Marks a single notification as seen """
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.seen = True
    notification.save()
    return redirect('notifications')

def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return redirect('notifications')

