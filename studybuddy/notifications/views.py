from notifications.models import Notification
from profile_users.models import Follow  
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

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
