from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, Follow
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer, FollowSerializer
from django.contrib.auth import get_user_model


User = get_user_model()

# Profile List and Detail Views
class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

User = get_user_model()

class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        """API for following a user"""
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prevent self-follow
        if request.user == following:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if follow already exists
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if not created:
            return Response({"status": "info", "message": "Already following or pending"}, status=status.HTTP_200_OK)

        # Check if recipient has a profile and whether it's public or private
        try:
            recipient_profile = following.profile
            if  recipient_profile.public_profile:
                follow.status = "accepted"
                follow.save()
                return Response({"status": "success", "message": "You are now following the user"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "success", "message": "Follow request sent and is awaiting approval"}, status=status.HTTP_201_CREATED)
        except Profile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, user_id):
        """API for unfollowing a user"""
        try:
            follow = Follow.objects.get(follower=request.user, following_id=user_id)
            follow.delete()
            return Response({"status": "success", "message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({"error": "Follow relationship does not exist"}, status=status.HTTP_400_BAD_REQUEST)
