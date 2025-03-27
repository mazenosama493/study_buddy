from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm, UserEditForm
from notes import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Follow

User = get_user_model()


def public_profile_view(request, username):
    """ View a public profile """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    if Follow.objects.filter(follower=request.user, following=user).exists():
        notes = user.note_set.all()
    else:
        notes =user.note_set.filter(show_on_profile=False)
    if user.username == request.user.username:
        return redirect('profile_view')

    return render(request, 'user_profiles/public_profile.html', {
        'profile': profile,
        'notes': notes,
        'is_following': is_following
    })


@login_required
def profile_view(request):
    """ Display user's profile and notes """
    profile, created = Profile.objects.get_or_create(user=request.user)
    notes = request.user.note_set.all()
    return render(request, 'user_profiles/profile.html', {'profile': profile, 'notes': notes})


@login_required
def edit_profile(request):
    """ Allow user to edit profile details and update profile picture """
    profile = Profile.objects.get(user=request.user)
    user = request.user

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        picture_form = UserEditForm(request.POST, request.FILES, instance=user)

        if profile_form.is_valid() and picture_form.is_valid():
            profile_form.save()
            picture_form.save()
            # ✅ Redirect to profile after saving
            return redirect('profile_view')

    else:
        profile_form = ProfileForm(instance=profile)
        picture_form = UserEditForm(instance=user)

    return render(request, 'user_profiles/edit_profile.html', {
        'profile_form': profile_form,
        'picture_form': picture_form
    })


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('public_profile', username=user_to_follow.username)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('public_profile', username=user_to_unfollow.username)
