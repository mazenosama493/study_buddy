from django import forms
from users.models import CustomUser
from .models import Profile

class ProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['bio']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']
