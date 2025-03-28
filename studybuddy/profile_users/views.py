from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm, UserEditForm
from notes import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Follow
from notifications.signals import send_notification
from django.contrib import messages
from django.http import HttpResponse
from notifications.models import Notification


User = get_user_model()


def public_profile_view(request, username):
    """ View a public profile """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    
    # Check if there is an accepted follow relationship
    follow_instance = Follow.objects.filter(follower=request.user, following=user).first()
    
    is_following = follow_instance and follow_instance.status == 'accepted'
    is_pending = follow_instance and not follow_instance.status == 'pending'
    count_followers = Follow.objects.filter(following=user, status='accepted').count()

    # Show notes only if the follow request is accepted
    if is_following:
        notes = user.note_set.all()
    else:
        notes = user.note_set.filter(show_on_profile=True)  # Show only public notes

    # Redirect to own profile if user is viewing themselves
    if user == request.user:
        return redirect('profile_view')

    return render(request, 'user_profiles/public_profile.html', {
        'profile': profile,
        'notes': notes,
        'is_following': is_following,
        'is_pending': is_pending,
        'count_followers': count_followers
        
    })


@login_required
def profile_view(request):
    """ Display user's profile and notes """
    profile, created = Profile.objects.get_or_create(user=request.user)
    notes = request.user.note_set.all()
    followers = Follow.objects.filter(following=request.user, status='accepted').count()
    followerss = Follow.objects.filter(following=request.user, status='accepted')
    return render(request, 'user_profiles/profile.html', {'profile': profile, 'notes': notes, 'followerss': followerss, 'followers': followers})


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


#@login_required
#def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    if user_to_follow != request.user:
        Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    return redirect('public_profile', username=user_to_follow.username)


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('public_profile', username=user_to_unfollow.username)

@login_required
def follow_user(request, user_id):
    """ Send a follow request instead of instantly following """
    user_to_follow = get_object_or_404(User, id=user_id)

    # Check if a follow request already exists
    follow_request, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )

    if not created:
        messages.info(request, "Follow request already sent.")
    else:
        # Send a notification to the user for the follow request
        message = f"{request.user.username} has requested to follow you."
        send_notification(request.user, user_to_follow, 'follow_request', message)

        messages.success(request, "Follow request sent successfully.")

    return redirect('public_profile', username=user_to_follow.username)

@login_required
def accept_follow_request(request, follow_id):
    """ Accept a follow request and notify the user """
    follow_request = get_object_or_404(Follow, id=follow_id, following=request.user)

    if follow_request.status == 'pending':
        follow_request.status = 'accepted'
        follow_request.save()

        message = f"{request.user.username} has accepted your follow request."
        send_notification(request.user, follow_request.follower, 'follow_accepted', message)

        messages.success(request, "Follow request accepted.")
    return redirect('notifications')

@login_required
def reject_follow_request(request, follow_id):
    """ Reject a follow request and notify the user """
    follow_request = get_object_or_404(Follow, id=follow_id, following=request.user)

    if follow_request.status == 'pending':
        follow_request.status = 'rejected'
        follow_request.delete()


        message = f"{request.user.username} has rejected your follow request."
        send_notification(request.user, follow_request.follower, 'follow_rejected', message)

        messages.info(request, "Follow request rejected.")

    return redirect('notifications')

def followers_view(request):
    """ Display a list of followers """
    followers = Follow.objects.filter(following=request.user, status='accepted')
    return render(request, 'user_profiles/followers.html', {'followers': followers})

def remove_follower(request, follow_id):
    """ Remove a follower """
    try:
        follow_instance = Follow.objects.get(id=follow_id, following=request.user, status='accepted')
        follow_instance.delete()
        return redirect('profile_view')
    except Follow.DoesNotExist:
        return HttpResponse("Follower not found or already removed.", status=404)




