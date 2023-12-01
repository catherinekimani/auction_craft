from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegistrationForm(UserCreationForm):

    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['user_bio','user_profile']
        
class ProfileUpdateForm(forms.ModelForm):
    user_bio = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Profile
        exclude = ('location', )