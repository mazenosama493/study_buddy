from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer

# Custom Registration View
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Login and Token Views (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass  # Uses the default behavior

class CustomTokenRefreshView(TokenRefreshView):
    pass  # Uses the default behavior

# Get User Profile (Authenticated Users Only)
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
