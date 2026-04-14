from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, get_user_model, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from .models import Profile
from .forms import CustomUserCreationForm, ProfileForm, CompleteProfileForm
from .serializers import (
    UserSerializer,
    MyTokenObtainPairSerializer,
    RegisterSerializer,
)

from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()


# -------- JWT Token API View --------

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# -------- Register API View --------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


# -------- User List API (Authenticated) --------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_list_api(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


# -------- Current User Info API --------

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user_info(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# -------- Complete Profile API (PATCH) --------

@api_view(['POST', 'PATCH'])
@permission_classes([IsAuthenticated])
def complete_profile_api(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = CompleteProfileForm(request.data, request.FILES, instance=profile)
    if form.is_valid():
        form.save()
        return Response({'message': 'Profile completed successfully'}, status=status.HTTP_200_OK)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


# -------- UI Views --------

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            auth_user = authenticate(username=user.username, password=request.POST['password1'])
            if auth_user:
                login(request, auth_user)
                profile = auth_user.profile
                profile.full_name = profile_form.cleaned_data.get('full_name', '')
                profile.address = profile_form.cleaned_data.get('address', '')
                profile.phone_number = profile_form.cleaned_data.get('phone_number', '')
                if request.FILES.get('profile_picture'):
                    profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                return redirect('home')
            else:
                # fallback: logout and show error or handle accordingly
                logout(request)
                return render(request, 'accounts/register.html', {
                    'user_form': user_form,
                    'profile_form': profile_form,
                    'error': 'Authentication failed after registration.'
                })
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'form': form})
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def home_view(request):
    profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'accounts/home.html', {'profile': profile})


@login_required
def complete_profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    if profile.phone_number:
        return redirect('home')

    if request.method == 'POST':
        form = CompleteProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CompleteProfileForm(instance=profile)

    return render(request, 'accounts/complete_profile.html', {'form': form})
