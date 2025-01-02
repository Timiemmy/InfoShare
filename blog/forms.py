from django import forms 
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content','category', 'status', 'image')


class SearchForm(forms.Form):
    query = forms.CharField()