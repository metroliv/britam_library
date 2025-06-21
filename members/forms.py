from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import MemberProfile


class CustomUserCreationForm(UserCreationForm):
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        return password2

    class Meta:
        model = User
        fields = ("username", "password1", "password2")



class MemberProfileForm(forms.ModelForm):
    class Meta:
        model = MemberProfile
        fields = ['phone', 'address', 'profile_image']
