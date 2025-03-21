from django.contrib import admin
from django import forms
from .models import CustomUser

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get("role")
        subject_category = cleaned_data.get("subject_category")
        grade_level = cleaned_data.get("grade_level")

        if role == "teacher" and grade_level:
            self.add_error("grade_level", "Teachers cannot have a grade level.")
        if role == "student" and subject_category:
            self.add_error("subject_category", "Students cannot have a subject category.")

        return cleaned_data

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserAdminForm
    list_display = ('username', 'email', 'role', 'subject_category', 'grade_level')
    fields = ('username', 'email', 'password', 'role', 'subject_category', 'grade_level', 'bio', 'profile_picture')

admin.site.register(CustomUser, CustomUserAdmin)
