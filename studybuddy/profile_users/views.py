from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm, UserEditForm, StudentEditForm, TeacherEditForm
from notes import models
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import Follow
from notifications.signals import send_notification
from django.contrib import messages
from django.http import HttpResponse
from notifications.models import Notification
from notes.models import Note
from notifications.views import has_unseen_notifications

User = get_user_model()


def public_profile_view(request, username):
    """ View a public profile """
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    role=get_object_or_404(User, username=username).role
    if role == 'student':
        form=grade_level=get_object_or_404(User, username=username).grade_level
    else:
        form=subject_category=get_object_or_404(User, username=username).subject_category
    GRADE_CHOICES = Note.GRADE_CHOICES
    SUBJECT_CHOICES = Note.SUBJECT_CHOICES
    
    # Check if there is a follow relationship
    follow_instance = Follow.objects.filter(follower=request.user, following=user).first()
    
    is_following = follow_instance and follow_instance.status == 'accepted'
    is_pending = follow_instance and follow_instance.status == 'pending'
    count_followers = Follow.objects.filter(following=user, status='accepted').count()

    # Show notes only if the follow request is accepted
    if is_following:
        notes = user.note_set.all().order_by('-created_at')
    else:
        notes = user.note_set.filter(show_on_profile=True).order_by('-created_at') # Show only public notes

    # Redirect to own profile if user is viewing themselves
    if user == request.user:
        return redirect('profile_view')

    notes, grade_filter, subject_filter =filter_notes(notes, request)

    return render(request, 'user_profiles/public_profile.html', {
        'profile': profile,
        'notes': notes,
        'grade_filter': grade_filter,
        'subject_filter': subject_filter,
        'is_following': is_following,
        'is_pending': is_pending,
        'count_followers': count_followers,
        'GRADE_CHOICES': GRADE_CHOICES,
        'SUBJECT_CHOICES': SUBJECT_CHOICES,
        'has_unseen_notifications': has_unseen_notifications(request.user),
        'form': form,
        'role': role
        
    })


@login_required
def profile_view(request):
    GRADE_CHOICES = Note.GRADE_CHOICES
    SUBJECT_CHOICES = Note.SUBJECT_CHOICES
    """ Display user's profile and notes """
    profile, created = Profile.objects.get_or_create(user=request.user)
    notes = request.user.note_set.all().order_by('-created_at')
    role=get_object_or_404(User, username=request.user.username).role
    if role == 'student':
        form=grade_level=get_object_or_404(User, username=request.user.username).grade_level
    else:
        form=subject_category=get_object_or_404(User, username=request.user.username).subject_category
    notes, grade_filter, subject_filter =filter_notes(notes, request)
    followers= Follow.objects.filter(following=request.user, status='accepted').count()
    followerss = Follow.objects.filter(following=request.user, status='accepted')
    
    
    
    return render(request, 'user_profiles/profile.html',
     {
        'profile': profile,
        'notes': notes,
        'followerss': followerss,
        'followers': followers,
        'GRADE_CHOICES': GRADE_CHOICES,
        'SUBJECT_CHOICES': SUBJECT_CHOICES,
        'grade_filter':grade_filter,
        'subject_filter': subject_filter,
        'form': form ,
        'has_unseen_notifications': has_unseen_notifications(request.user),
        'role': role
     })


@login_required
def edit_profile(request):
    """ Allow user to edit profile details, username, profile picture, and role-specific fields """
    profile = Profile.objects.get(user=request.user)
    user = request.user
    role = user.role
    
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        user_form = UserEditForm(request.POST, request.FILES, instance=user)
        
        # Role-specific form
        if role == 'student':
            role_form = StudentEditForm(request.POST, instance=user)
        else:  # teacher
            role_form = TeacherEditForm(request.POST, instance=user)
            
        if profile_form.is_valid() and user_form.is_valid() and role_form.is_valid():
            profile_form.save()
            user_form.save()
            role_form.save()
            return redirect('profile_view')
    else:
        profile_form = ProfileForm(instance=profile)
        user_form = UserEditForm(instance=user)
        
        # Role-specific form
        if role == 'student':
            role_form = StudentEditForm(instance=user)
        else:  # teacher
            role_form = TeacherEditForm(instance=user)

    return render(request, 'user_profiles/edit_profile.html', {
        'profile_form': profile_form,
        'user_form': user_form,
        'role_form': role_form,
        'role': role,
        'has_unseen_notifications': has_unseen_notifications(request.user)
    })


@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    return redirect('public_profile', username=user_to_unfollow.username)

@login_required
def cancel_follow_request(request, user_id):
    """ Cancel a pending follow request """
    user_to_unfollow = get_object_or_404(User, id=user_id)
    follow_request = get_object_or_404(Follow, follower=request.user, following=user_to_unfollow, status='pending')
    
    # Delete the follow request
    follow_request.delete()
    
    # Delete any related notifications
    Notification.objects.filter(
        sender=request.user, 
        recipient=user_to_unfollow, 
        notification_type="follow_request"
    ).delete()
    
    messages.info(request, "Follow request canceled.")
    return redirect('public_profile', username=user_to_unfollow.username)

@login_required
def follow_user(request, user_id):
    """ Follow a user instantly if their profile is public, otherwise send a follow request """
    user_to_follow = get_object_or_404(User, id=user_id)
    profile = get_object_or_404(Profile, user=user_to_follow)

    # Delete any existing rejected follow request
    Follow.objects.filter(
        follower=request.user,
        following=user_to_follow,
        status='rejected'
    ).delete()

    follow_request, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow,
        defaults={'status': 'pending'}
    )

    if profile.public_profile:
        follow_request.status = 'accepted'
        follow_request.save()
        messages.success(request, f"You are now following {user_to_follow.username}.")
        message = f"{request.user.username} is now following you."
        send_notification(request.user, user_to_follow, 'follow', message)
    else:
        if created:
            message = f"{request.user.username} has requested to follow you."
            send_notification(request.user, user_to_follow, 'follow_request', message)
            messages.success(request, "Follow request sent.")
        else:
            messages.info(request, "Follow request already sent.")

    return redirect('public_profile', username=user_to_follow.username)

@login_required
def accept_follow_request(request, follow_id):
    """ Accept a follow request and notify the user """
    follow_request = get_object_or_404(Follow, id=follow_id, following=request.user)

    if follow_request.status == 'pending':
        follow_request.status = 'accepted'
        follow_request.save()

        Notification.objects.filter(
            sender=follow_request.follower, 
            recipient=request.user, 
            notification_type="follow_request"
        ).delete()

        message = f"{request.user.username} has accepted your follow request."
        message2=f"{follow_request.follower.username} is now following you."
        send_notification(request.user, follow_request.follower, 'follow_accepted', message)
        send_notification(follow_request.follower, request.user, 'follow', message2)
        messages.success(request, "Follow request accepted.")

    return redirect('notifications')

@login_required
def reject_follow_request(request, follow_id):
    """ Reject a follow request and notify the user """
    follow_request = get_object_or_404(Follow, id=follow_id, following=request.user)

    if follow_request.status == 'pending':
        follow_request.status = 'rejected'
        follow_request.save()

        Notification.objects.filter(
            sender=follow_request.follower, 
            recipient=request.user, 
            notification_type="follow_request"
        ).delete()


        message = f"{request.user.username} has rejected your follow request."
        message2=f"{follow_request.follower.username} request has been rejected."
        send_notification(request.user, follow_request.follower, 'follow_rejected', message)
        send_notification(follow_request.follower, request.user, 'follow_rejected', message2)
        messages.info(request, "Follow request rejected.")


    return redirect('notifications')
def remove_follower(request, follow_id):
    """ Remove a follower """
    try:
        follow_instance = Follow.objects.get(id=follow_id, following=request.user, status='accepted')
        follow_instance.delete()
        return redirect('profile_view')
    except Follow.DoesNotExist:
        return HttpResponse("Follower not found or already removed.", status=404)


@login_required
def toggle_profile_privacy(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile.public_profile = not profile.public_profile
    profile.save()
    return redirect('profile_view')


def filter_notes(notes, request):
    
    """Filter notes by grade level and subject"""
    grade_filter = request.GET.get('grade_level', '')
    subject_filter = request.GET.get('subject', '')

    if grade_filter:
        notes = notes.filter(grade_level=grade_filter).order_by('-created_at')
    if subject_filter:
        notes = notes.filter(subject=subject_filter).order_by('-created_at')
    
    return notes, grade_filter, subject_filter







