from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from LogMyFit.models import Activity


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['type', 'duration', 'amount', 'activity_date']
        widgets = {
            'type': forms.Select(choices=Activity.TYPE_CHOICES),
            'activity_date': forms.DateInput(attrs={'type': 'date'}),
        }
