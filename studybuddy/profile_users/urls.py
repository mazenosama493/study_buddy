from django.urls import path
from .views import profile_view, edit_profile, public_profile_view, follow_user, accept_follow_request, reject_follow_request, followers_view,remove_follower, toggle_profile_privacy
from . import views

urlpatterns = [
    path('', profile_view, name='profile_view'),
    path('edit/', edit_profile, name='edit_profile'),
    path('toggle-privacy/',toggle_profile_privacy, name='toggle_profile_privacy'),
    path('<str:username>/', public_profile_view, name='public_profile'),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('accept-follow/<int:follow_id>/', accept_follow_request, name='accept_follow_request'),
    path('reject-follow/<int:follow_id>/', reject_follow_request, name='reject_follow_request'),
    path('followers/', views.followers_view, name='followers_view'),
    path('remove-follower/<int:follow_id>/', remove_follower, name='remove_follower'),
]
