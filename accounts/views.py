from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import EmailUserCreationForm, UsernameOrEmailAuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = EmailUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')

            user = authenticate(
                request,
                username=email,   # still email for auth
                password=password
            )

            login(request, user)

            # messages.success(
            #     request,
            #     f'Account created! Welcome, {user.username}!'
            # )

            return redirect('recommendations:home')
    else:
        form = EmailUserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UsernameOrEmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request,
                username=identifier,
                password=password
            )

            if user is not None:
                login(request, user)
                # messages.success(
                #     request,
                #     f'Welcome back, {user.username}!'
                # )
                return redirect('recommendations:home')
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UsernameOrEmailAuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')