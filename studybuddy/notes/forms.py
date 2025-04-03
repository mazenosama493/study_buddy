from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'file', 'grade_level', 'subject', 'show_on_profile','id']
