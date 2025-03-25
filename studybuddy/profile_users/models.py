from django.db import models
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    shared_notes = models.ManyToManyField(Note, blank=True, related_name="shared_profiles")
    #public_profile = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
