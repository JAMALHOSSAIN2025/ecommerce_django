# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# ---------- Custom User Creation Form ----------
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # ✅ password1, password2 অবশ্যই রাখতে হবে

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


# ---------- Custom User Change Form (for admin) ----------
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


# ---------- Profile Form (used in profile creation or update) ----------
class ProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'address', 'profile_picture']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


# ---------- Profile Completion Form (used in complete_profile_view) ----------
class CompleteProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['address', 'profile_picture']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
