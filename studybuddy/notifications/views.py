from notifications.models import Notification
from profile_users.models import Follow  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db import models

def has_unseen_notifications(user):
    return Notification.objects.filter(recipient=user).filter(models.Q(seen=False)).exists()

@login_required
def notifications_view(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    context = {
        'notifications': notifications,
        'has_unseen_notifications': has_unseen_notifications(request.user)
    }
    return render(request, 'notifications/notifications.html', context)

@login_required
def mark_notifications_as_seen(request):
    Notification.objects.filter(recipient=request.user).update(seen=True, is_read=True)
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user).update(seen=True)
    return redirect('notifications')

@login_required
def mark_single_notification_as_seen(request, notification_id):
    if request.method == 'POST':
        notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
        notification.seen = True
        notification.save()
    return redirect('notifications')

# Note: The actual accept_follow_request and reject_follow_request functions
# are imported from profile_users.views in the urls.py file
    
def delete_notification(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, recipient=request.user)
    notification.delete()
    return redirect('notifications')

