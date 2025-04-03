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
        """ API for following a user """
        try:
            following = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Prevent self-follow
        if request.user == following:
            return Response({"error": "You cannot follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if follow already exists
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following)

        if created:
            return Response({"status": "success", "message": "Follow request sent"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "info", "message": "Already following"}, status=status.HTTP_200_OK)
    
    def delete(self, request, user_id):
        """ API for unfollowing a user """
        try:
            follow = Follow.objects.get(follower=request.user, following_id=user_id)
            follow.delete()
            return Response({"status": "success", "message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({"error": "Follow relationship does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, user_id):
        """ API for unfollowing a user """
        try:
            follow = Follow.objects.get(follower=user_id.user, following_id=request.user.id)
            follow.delete()
            return Response({"status": "success", "message": "Unfollowed successfully"}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({"error": "Follow relationship does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class RemoveFollowerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id):
        """ API for removing a follower """
        try:
            follow = Follow.objects.get(follower_id=user_id, following=request.user)
            follow.delete()
            return Response({"status": "success", "message": "Follower removed successfully"}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({"error": "This user is not following you"}, status=status.HTTP_400_BAD_REQUEST)

