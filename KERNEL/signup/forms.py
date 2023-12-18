from django import forms
from .models import UserTable

class UserTableForm(forms.ModelForm):
    class Meta:
        model = UserTable
        fields = ['username', 'password', 'name', 'phone', 'email', 'area', 'gender']