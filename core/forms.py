from django import forms
from django.contrib.auth.models import User
from .models import UserRole,Job,Application

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=UserRole.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']



class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'company_name', 'location', 'description']




class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']

