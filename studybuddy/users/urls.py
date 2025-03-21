from django.urls import path
from .views import register, CustomLoginView, logout_view, profile
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenVerifyView
from .api_views import RegisterUserView, CustomTokenObtainPairView, CustomTokenRefreshView, UserProfileView



urlpatterns = [
    path('register/', register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('api/register/', RegisterUserView.as_view(), name='api-register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='api-token'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='api-token-refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='api-token-verify'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
]
