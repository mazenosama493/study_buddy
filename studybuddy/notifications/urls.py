from django.urls import path
from .views import notifications_view, mark_single_notification_as_seen, mark_notifications_as_seen, delete_notification
from .api_views import NotificationListCreateView, NotificationDetailView


urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('notifications/mark-all-as-seen/', mark_notifications_as_seen, name='mark_notifications_as_seen'),  
    path('notifications/mark-as-seen/<int:notification_id>/', mark_single_notification_as_seen, name='mark_single_notification_as_seen'),
    path('delete/<int:notification_id>/', delete_notification, name='delete_notification'),
    path('api/', NotificationListCreateView.as_view(), name='list_create_notifications'),
    path('api/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
]
