from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import CustomUser
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import UserSerializer, ProfileUpdateSerializer

# Custom Registration View
class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class ProfileUpdateAPIView(generics.UpdateAPIView):
    """ API to update profile picture, username, grade level (students), and subject category (teachers) """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Allow image uploads

    def get_object(self):
        """ Ensure users can only update their own profile """
        return self.request.user

# Login and Token Views (JWT)
class CustomTokenObtainPairView(TokenObtainPairView):
    pass  

class CustomTokenRefreshView(TokenRefreshView):
    pass  

