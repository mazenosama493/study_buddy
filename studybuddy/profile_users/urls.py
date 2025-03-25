from django.urls import path
from .views import profile_view, edit_profile, public_profile_view

urlpatterns = [
    path('', profile_view, name='profile_view'),
    path('edit/', edit_profile, name='edit_profile'),
    path('<str:username>/', public_profile_view, name='public_profile'),
]
