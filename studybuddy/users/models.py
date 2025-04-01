from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from notes.models import Note

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]
    SUBJECT_CATEGORIES = Note.SUBJECT_CHOICES
    GRADE_LEVELS = Note.GRADE_CHOICES
    subject_category = models.CharField(max_length=20, choices=SUBJECT_CATEGORIES, blank=True, null=True , default='mathematics')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    grade_level = models.CharField(max_length=20, choices=GRADE_LEVELS, blank=True, null=True, default='first')
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)


    def clean(self):
        """ Validate that a user cannot have both subject_category and grade_level """
        if self.role == 'teacher' and self.grade_level:
            raise ValidationError("Teachers cannot have a grade level.")
        if self.role == 'student' and self.subject_category:
            raise ValidationError("Students cannot have a subject category.")

    def __str__(self):
        return self.username
