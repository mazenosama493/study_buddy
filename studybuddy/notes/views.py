from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note, Like, Dislike, Comment
from .forms import NoteForm
from django.db import models
from django.db.models import Q
from django.contrib import messages
from notifications.models import Notification


@login_required
def notes_list(request):
    """ Show all notes, allow filtering by grade, subject, and username """

    user = request.user
    notes = Note.objects.filter(show_on_profile=False)

    # Define grade and subject choices correctly as (value, label) tuples
    GRADE_CHOICES = [
        ('first', 'Grade 1'),
        ('second', 'Grade 2'),
        ('third', 'Grade 3'),
        ('fourth', 'Grade 4'),
        ('fifth', 'Grade 5'),
        ('sixth', 'Grade 6'),
        ('seventh', 'Grade 7'),
        ('eighth', 'Grade 8'),
        ('ninth', 'Grade 9'),
        ('tenth', 'Grade 10'),
        ('eleventh', 'Grade 11'),
        ('twelfth', 'Grade 12'),
    ]

    SUBJECT_CHOICES = [
        ("mathematics", "Mathematics"), ("science", "Science"),
        ("history", "History"), ("english", "English"),
        ("computers", "Computer Science"), ("arts", "Arts")
    ]

    # Get filter values from request
    grade_filter = request.GET.get('grade_level', '')
    subject_filter = request.GET.get('subject', '')
    username_filter = request.GET.get('username', '')

    # Apply filters if selected
    if grade_filter:
        notes = notes.filter(grade_level=grade_filter)
    if subject_filter:
        notes = notes.filter(subject=subject_filter)
    if username_filter:
        notes = notes.filter(author__username__icontains=username_filter)

    # Prioritize notes based on user role
    if user.role == 'student':
        notes = sorted(notes, key=lambda note: (
            note.grade_level != user.grade_level, -note.created_at.timestamp()))
    elif user.role == 'teacher':
        notes = sorted(notes, key=lambda note: (
            note.subject != user.subject_category, -note.created_at.timestamp()))

    return render(request, 'notes/notes_list.html', {
        'notes': notes,
        'grade_filter': grade_filter,
        'subject_filter': subject_filter,
        'username_filter': username_filter,
        'GRADE_CHOICES': GRADE_CHOICES,
        'SUBJECT_CHOICES': SUBJECT_CHOICES
    })


@login_required
def note_detail(request, note_id):
    """ Show a single note """
    note = get_object_or_404(Note, id=note_id)
    top_level_comments = note.comments.filter(
        parent__isnull=True)  # Only top-level comments
    return render(request, 'notes/note_detail.html', {
        'note': note,
        'top_level_comments': top_level_comments
    })


@login_required
def create_note(request):
    """ Create a new note """
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.save()
            form.save_m2m() 
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def edit_note(request, note_id):
    """ Edit an existing note """
    note = get_object_or_404(Note, id=note_id, author=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect('notes_list')
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_form.html', {'form': form})


@login_required
def delete_note(request, note_id):
    """ Show confirmation page before deleting a note """
    note = get_object_or_404(Note, id=note_id, author=request.user)

    if request.method == "POST":  # If user confirms deletion
        note.delete()
        messages.success(request, "Your note has been successfully deleted.")
        return redirect('notes_list')

    return render(request, 'notes/confirm_delete.html', {'note': note})


@login_required
def like_note(request, note_id):
    """ Toggle like on a note and notify the author """
    note = get_object_or_404(Note, id=note_id)
    like, created = Like.objects.get_or_create(user=request.user, note=note)

    if not created:
        like.delete()
    else:
        Dislike.objects.filter(user=request.user, note=note).delete()

        if note.author != request.user:
            Notification.objects.create(
                recipient=note.author,  # **Receiver (Note's Author)**
                sender=request.user,  # **Who liked the note**
                note=note,
                notification_type="like",
                message = f"{request.user.username} liked your note: {note.title}."
            )

    return redirect('note_detail', note_id=note.id)



@login_required
def dislike_note(request, note_id):
    """ Toggle dislike on a note """
    note = get_object_or_404(Note, id=note_id)
    dislike, created = Dislike.objects.get_or_create(
        user=request.user, note=note)

    if not created:
        dislike.delete()  #
    else:
        Like.objects.filter(user=request.user, note=note).delete()
        if note.author != request.user:
            Notification.objects.create(
                recipient=note.author, 
                sender=request.user,  
                note=note,
                notification_type="dislike",
                message = f"{request.user.username} disliked your note: {note.title}."
            )

    return redirect('note_detail', note_id=note.id)


@login_required
def add_comment(request, note_id):
    """ Add a comment to a note """
    note = get_object_or_404(Note, id=note_id)
    content = request.POST.get('content')

    if content:
        Comment.objects.create(user=request.user, note=note,content=content)
        if note.author != request.user:
            Notification.objects.create(
                recipient=note.author,
                sender=request.user,
                note=note,
                notification_type="comment",
                message = f"{request.user.username} commented your note: {note.title}."
            )

    return redirect('note_detail', note_id=note.id)


@login_required
def add_reply(request, note_id, comment_id):
    """ Add a reply to a comment """
    note = get_object_or_404(Note, id=note_id)
    parent_comment = get_object_or_404(Comment, id=comment_id, note=note)
    content = request.POST.get('content')

    if content:
        # Create a reply and associate it with the parent comment
        Comment.objects.create(
            user=request.user,
            note=note,
            parent=parent_comment,
            content=content
        )
        if parent_comment.user != request.user:
            Notification.objects.create(
                recipient=parent_comment.user,
                sender=request.user,
                note=note,
                notification_type="comment",
                message = f"{request.user.username} replied on your comment on this note: {note.title}."
            )
        
        if parent_comment.user != request.user and note.author != request.user:
            Notification.objects.create(
                recipient=note.author,
                sender=request.user,
                note=note,
                notification_type="comment",
                message = f"{request.user.username} commented your note: {note.title}."
            )


    return redirect('note_detail', note_id=note.id)
