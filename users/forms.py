from django import forms
from polls.models import Profile
from django.contrib.auth.models import User

class ProfilePicUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('image',)


class UserProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email')
    
