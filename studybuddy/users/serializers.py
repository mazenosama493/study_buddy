from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        profile_picture = serializers.ImageField(required=False)
        fields = ['id', 'username', 'email', 'password', 'role', 'subject_category', 'grade_level', 'profile_picture']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=validated_data['role'],
            subject_category=validated_data.get('subject_category', None),
            grade_level=validated_data.get('grade_level', None),
            profile_picture=validated_data.get('profile_picture', None),
        )
        return user
    def validate(self, data):
        role = data.get('role')
        subject = data.get('subject_category')
        grade = data.get('grade_level')

        if role == 'student' and subject:
            raise serializers.ValidationError("Students should not have a subject category.")
        if role == 'teacher' and grade:
            raise serializers.ValidationError("Teachers should not have a grade level.")
        return data

class ProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        profile_picture = serializers.ImageField(required=False)
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

