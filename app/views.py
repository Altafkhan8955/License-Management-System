from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import (
    LicenseCreationForm, LicenseValidationForm, LicenseRevocationForm,
    RegisterForm, CustomLoginForm
)
from .models import License, LicenseLog

def home(request):
    return render(request, 'home.html')

@login_required
def validate_license(request):
    if request.method == 'POST':
        form = LicenseValidationForm(request.POST)
        if form.is_valid():
            license_key = form.cleaned_data['license_key']
            try:
                license = License.objects.get(key=license_key)
                if license.is_valid():
                    LicenseLog.objects.create(license=license, is_successful=True, message="Validation successful")
                    messages.success(request, 'License is valid.')
                else:
                    messages.error(request, 'License is invalid or expired.')
            except License.DoesNotExist:
                messages.error(request, 'License not found.')
    else:
        form = LicenseValidationForm()
    
    return render(request, 'validate_license.html', {'form': form})

@login_required
def create_license(request):
    if request.method == 'POST':
        form = LicenseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'License created successfully.')
            return redirect('home')
    else:
        form = LicenseCreationForm()
    
    return render(request, 'create_license.html', {'form': form})

@login_required
def revoke_license(request):
    if request.method == 'POST':
        form = LicenseRevocationForm(request.POST)
        if form.is_valid():
            license_key = form.cleaned_data['license_key']
            try:
                license = License.objects.get(key=license_key)
                license.status = 'revoked'
                license.save()
                messages.success(request, 'License revoked successfully.')
            except License.DoesNotExist:
                messages.error(request, 'License not found.')
    else:
        form = LicenseRevocationForm()
    
    return render(request, 'revoke_license.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomLoginForm()
    
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout successful.')
    return redirect('login')
