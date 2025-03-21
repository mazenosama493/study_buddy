from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    SUBJECT_CATEGORIES = [
        ('math', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
        ('english', 'English'),
        ('computers', 'Computer Science'),
        ('arts', 'Arts'),
    ]
    GRADE_LEVELS = [
        ('first', 'First Grade'),
        ('second', 'Second Grade'),
        ('third', 'Third Grade'),
        ('fourth', 'Fourth Grade'),
        ('fifth', 'Fifth Grade'),
        ('sixth', 'Sixth Grade'),
        ('seventh', 'Seventh Grade'),
        ('eighth', 'Eighth Grade'),
        ('ninth', 'Ninth Grade'),
        ('tenth', 'Tenth Grade'),
        ('eleventh', 'Eleventh Grade'),
        ('twelfth', 'Twelfth Grade'),
    ]
    subject_category = models.CharField(max_length=20, choices=SUBJECT_CATEGORIES, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    grade_level = models.CharField(max_length=20, choices=GRADE_LEVELS, blank=True, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)


    def clean(self):
        """ Validate that a user cannot have both subject_category and grade_level """
        if self.role == 'teacher' and self.grade_level:
            raise ValidationError("Teachers cannot have a grade level.")
        if self.role == 'student' and self.subject_category:
            raise ValidationError("Students cannot have a subject category.")

    def __str__(self):
        return self.username
