from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# Create your views here.

def login_view(request):
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    auth_login(request, user)
                    messages.success(request, f'Welcome {username}!')
                    return redirect('home')
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            form = AuthenticationForm()
        return render(request, 'auths/login.html', {'form': form})

def register_view(request):
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                auth_login(request, user)
                messages.success(request, 'Registration successful.')
                return redirect('home')
            else:
                messages.error(request, 'Unsuccessful registration. Invalid information.')
        else:
            form = UserCreationForm()
        return render(request, 'auths/register.html', {'form': form})

def logout_view(request):
        auth_logout(request)
        messages.success(request, 'You have been logged out.')
        return redirect('login')