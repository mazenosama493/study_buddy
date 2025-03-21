from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    profile_picture = forms.ImageField(required=False)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    subject_category = forms.ChoiceField(
        choices=[('', 'Select a subject')] + CustomUser.SUBJECT_CATEGORIES, 
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'subject_category'}),
        required=False
    )
    grade_level = forms.ChoiceField(
        choices=[('', 'Select a grade')] + CustomUser.GRADE_LEVELS,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'grade_level'}),
        required=False
    )


    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture', 'role', 'subject_category', 'grade_level']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'role' in self.data:
            role = self.data.get('role')
            if role == 'teacher':
                self.fields['subject_category'].required = True
                self.fields['grade_level'].required = False
            elif role == 'student':
                self.fields['subject_category'].required = False
                self.fields['grade_level'].required = True
    

