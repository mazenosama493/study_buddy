from rest_framework import generics, permissions
from .models import Note, Comment, Like, Dislike
from .serializers import NoteSerializer, CommentSerializer, LikeSerializer, DislikeSerializer
from django.core.exceptions import PermissionDenied
from profile_users.models import Follow
from rest_framework.parsers import MultiPartParser, FormParser

class NoteListCreateView(generics.ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        note = super().get_object()
        user = self.request.user

        # Restrict access to view
        if note.show_on_profile:
            if note.author != user:
                if not Follow.objects.filter(follower=user, following=note.author).exists():
                    raise PermissionDenied("You are not allowed to view this note.")

        # Restrict update and delete
        if self.request.method in ['PUT', 'PATCH', 'DELETE'] and note.author != user:
            raise PermissionDenied("You are not allowed to modify or delete this note.")

        return note
# Comment API
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        note = serializer.validated_data.get('note')
        parent = serializer.validated_data.get('parent', None)
        user = self.request.user

        # Visibility validation
        if not note:
            raise PermissionDenied("Note is required to comment.")
        if note.show_on_profile:
            if note.author != user:
                if not Follow.objects.filter(follower=user, following=note.author).exists():
                    raise PermissionDenied("You are not allowed to comment on this note.")

        # Reply validation
        if parent:
            if parent.note != note:
                raise PermissionDenied("You cannot reply to a comment on a different note.")

        serializer.save(user=user)



# Like API
class LikeCreateDeleteView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    

    def perform_create(self, serializer):
        user = self.request.user
        note = serializer.validated_data.get('note')

        if not note:
            raise PermissionDenied("Note is required to like.")

        if note.show_on_profile:
            if note.author != user:
                if not Follow.objects.filter(follower=user, following=note.author).exists():
                    raise PermissionDenied("You are not allowed to like this note .")

        existing_like = Like.objects.filter(user=user, note=note).first()
        if existing_like:
            existing_like.delete()  # Unlike
        else:
            # Remove existing dislike (if any)
            Dislike.objects.filter(user=user, note=note).delete()

        serializer.save(user=user)


class DislikeCreateDeleteView(generics.CreateAPIView):
    queryset = Dislike.objects.all()
    serializer_class = DislikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        note = serializer.validated_data.get('note')

        if not note:
            raise PermissionDenied("Note is required to dislike.")

        if note.show_on_profile:
            if note.author != user:
                if not Follow.objects.filter(follower=user, following=note.author).exists():
                    raise PermissionDenied("You are not allowed to dislike this note .")

        existing_dislike = Dislike.objects.filter(user=user, note=note).first()
        if existing_dislike:
            existing_dislike.delete()  # Remove dislike
        else:
            # Remove existing like (if any)
            Like.objects.filter(user=user, note=note).delete()

        serializer.save(user=user)