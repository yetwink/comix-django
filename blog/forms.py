from django import forms
from .models import Comics, Volume, Chapter, Picture, Comment, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField

class ComicsForm(forms.ModelForm):
    class Meta:
        model = Comics
        fields = ['title', 'description', 'artist', 'writer', 'poster', 'genres']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Напишите название комикса'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Описание комикса'
            }),
            'artist': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Напишите художника'
            }),
            'writer': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Напишите сценариста'
            }),
            'poster': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light',
            }),
            'genres': forms.SelectMultiple(attrs={
                'class': 'form-select bg-dark text-light'
            })

        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['number']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light',
                'placeholder': 'Номер главы'
        })
        }

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control bg-dark text-light',
            }),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))


class RegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(label='Пароль2', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтвердите пароль'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Имя пользователя'
    }))
    first_name = forms.CharField( widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваше имя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша фамилия'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ваша почта'
    }))
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',
                  'password1', 'password2', 'captcha']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            })
        }

class ProfileForm(forms.ModelForm):
    bio = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    photo = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))
    profile_bg = forms.ImageField(required=True, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Profile
        fields = ['bio', 'photo', 'profile_bg']



