from django.urls import path
from .views import notifications_view, mark_single_notification_as_seen, mark_notifications_as_seen

urlpatterns = [
    path('', notifications_view, name='notifications'),
     path('notifications/mark-all-as-seen/', mark_notifications_as_seen, name='mark_notifications_as_seen'),  
    path('notifications/mark-as-seen/<int:notification_id>/', mark_single_notification_as_seen, name='mark_single_notification_as_seen'),

]
