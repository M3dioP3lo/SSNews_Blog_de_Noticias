from django import forms
from .models import Profile
from .models import Blog, Comment
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image']

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['titulo', 'contenido', 'categoria', 'image']
        widgets = {
            'titulo': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Título del Blog'}),
            'contenido': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Contenido del Blog'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }