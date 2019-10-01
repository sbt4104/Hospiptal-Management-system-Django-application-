from django import forms
from django.contrib.auth.models import User
from account.models import UserProfileInfo , UserProfileInfo2
from api1.models import Schedules , Case

class SchedulesForm(forms.ModelForm):
    
    class Meta():
        model = Schedules
        fields = ('avlday','avltime')


class CaseForm(forms.ModelForm):

    class Meta():
        model = Case
        fields = ('doctor','appointday','appointtime')        

class Fromdoctodate(forms.ModelForm):

    class Meta():
        model = Case
        fields = ('doctor',)        

class Updatehelper(forms.ModelForm):

    class Meta():
        model = Case
        fields = ('prescription','status',)        