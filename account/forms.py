from django import forms
from django.contrib.auth.models import User
from account.models import UserProfileInfo , UserProfileInfo2

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('portfolio_site','profile_pic','contact','field')


class UserForm2(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')


class UserProfileInfoForm2(forms.ModelForm):
    class Meta():
        model = UserProfileInfo2
        fields = ('portfolio_site','profile_pic','contact')


class Searchprofession(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('field',)               