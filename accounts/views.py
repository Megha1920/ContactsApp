from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import CustomUserCreationForm, CustomLoginForm

def landing_page(request):
    return render(request, 'landing_page.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Use auth_login to avoid naming conflicts
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username}")
            user = authenticate(request, username=username, password=password)
            print(f"User authenticated: {user}")  # Should print the user object or None
            if user is not None:
                auth_login(request, user)
                return redirect('contacts:list_contacts')
            else:
                print(f"Authentication failed for user: {username}")
                form.add_error(None, 'Invalid username or password')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = CustomLoginForm()

    return render(request, 'login.html', {'form': form})