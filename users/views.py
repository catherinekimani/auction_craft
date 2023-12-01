from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileUpdateForm,ProfileForm
from .models import Profile
# Create your views here.
def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, f'Your account has been created. You can log in now!')
            return redirect('login')
    else:
        form = UserRegistrationForm()

    context = {'form': form}

    return render(request, 'users/register.html', context)

def profile(request):
    current_user = request.user
    
    profile = Profile.objects.filter(user_id = current_user.id).first()
    
    return render(request,'users/profile/profile.html',{"profile":profile})

def editprofile(request):
    
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST,instance=request.user)
        
        form = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if form.is_valid() and form.is_valid():
            
            form.save()
            
            form.save()
            
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
        form = ProfileUpdateForm(instance=request.user.profile)
        
    return render(request,'users/profile/edit.html',{'form':form})