from django import forms
from users.models import CustomUser
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Tell us about yourself...'}),
        }

class UserEditForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-input'}))
    profile_picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_picture']

class StudentEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['grade_level']
        widgets = {
            'grade_level': forms.Select(attrs={'class': 'form-input'}),
        }

class TeacherEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['subject_category']
        widgets = {
            'subject_category': forms.Select(attrs={'class': 'form-input'}),
        }