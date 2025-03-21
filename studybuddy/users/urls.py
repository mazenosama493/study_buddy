from django.urls import path
from .views import register, CustomLoginView, logout_view, profile
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]
