from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm
from notes import models
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

def public_profile_view(request, username):
    """ View a public profile """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # ✅ Show only public notes
    notes = user.note_set.all()

    return render(request, 'user_profiles/public_profile.html', {
        'profile': profile,
        'notes': notes
    })

@login_required
def profile_view(request):
    """ Display user's profile and notes """
    profile, created = Profile.objects.get_or_create(user=request.user)
    notes = request.user.note_set.all()
    return render(request, 'user_profiles/profile.html', {'profile': profile, 'notes': notes})

@login_required
def edit_profile(request):
    """ Allow user to edit profile details """
    profile = Profile.objects.get(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'user_profiles/edit_profile.html', {'form': form})
