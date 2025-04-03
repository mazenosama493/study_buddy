from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'role', 'subject_category', 'grade_level', 'bio', 'profile_picture']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role'],
            subject_category=validated_data.get('subject_category', None),
            grade_level=validated_data.get('grade_level', None),
            bio=validated_data.get('bio', ''),
            profile_picture=validated_data.get('profile_picture', None),
        )
        return user

from rest_framework import serializers
from .models import CustomUser

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture', 'grade_level', 'subject_category']

    def validate(self, data):
        """ Ensure students and teachers have the correct fields updated """
        user = self.instance  # Get the current user

        # If user is a student, they should not update subject_category
        if user.role == 'student' and 'subject_category' in data:
            raise serializers.ValidationError("Students cannot select a subject category.")

        # If user is a teacher, they should not update grade_level
        if user.role == 'teacher' and 'grade_level' in data:
            raise serializers.ValidationError("Teachers cannot select a grade level.")

        return data

