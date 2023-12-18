from django import forms
from .models import PostTable

class PostForm(forms.ModelForm):
    class Meta:
        model = PostTable
        fields = ['title', 'content']