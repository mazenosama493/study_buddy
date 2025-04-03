from rest_framework import serializers
from .models import Profile, Follow
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Profile
        fields = ['user', 'bio' ,'public_profile']

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.StringRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    status = serializers.ChoiceField(choices=Follow.STATUS_CHOICES, default='pending')

    class Meta:
        model = Follow
        fields = ['follower', 'following', 'status', 'created_at']
