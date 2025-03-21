from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

