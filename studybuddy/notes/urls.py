from django.urls import path
from . import views

urlpatterns = [
    path('', views.notes_list, name='notes_list'),
    path('<int:note_id>/', views.note_detail, name='note_detail'),
    path('create/', views.create_note, name='create_note'),
    path('<int:note_id>/edit/', views.edit_note, name='edit_note'),
    path('<int:note_id>/delete/', views.delete_note, name='delete_note'),
    path('<int:note_id>/like/', views.like_note, name='like_note'),
    path('<int:note_id>/dislike/', views.dislike_note, name='dislike_note'),
    path('<int:note_id>/comment/', views.add_comment, name='add_comment'),
]
