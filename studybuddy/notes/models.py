from django.db import models
from django.conf import settings  

class Note(models.Model):
    SUBJECT_CHOICES = [
        ('mathematics', 'Mathematics'),
        ('science', 'Science'),
        ('history', 'History'),
        ('english', 'English'),
        ('computers', 'Computer Science'),
        ('arts', 'Arts'),
    ]
    GRADE_CHOICES =[
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
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    grade_level = models.CharField(max_length=50,choices=GRADE_CHOICES, default='first') 
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default='mathematics') 
    show_on_profile = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.title} - {self.subject} ({self.grade_level})"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='dislikes')
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)  # ✅ Allows replies
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.note.title if self.note else "a reply"}'

