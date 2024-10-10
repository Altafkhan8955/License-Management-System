from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import License, User

class LicenseCreationForm(forms.ModelForm):
    class Meta:
        model = License
        fields = ['key', 'product_name', 'client_name', 'expiry_date']

class LicenseValidationForm(forms.Form):
    license_key = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Enter License Key'}))

class LicenseRevocationForm(forms.Form):
    license_key = forms.CharField(max_length=64, widget=forms.TextInput(attrs={'placeholder': 'Enter License Key to Revoke'}))

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'role']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
