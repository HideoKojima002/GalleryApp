from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField, CaptchaTextInput

from .models import *


class ImageForm(forms.ModelForm):
    tags_ = forms.CharField(label='Тeги', required=False,
                            widget=forms.TextInput(
                                attrs={
                                    'class': 'form-control',
                                    'id': 'floatingInput',
                                    'placeholder': 'Тeги',
                                }))
    image = forms.ImageField(label='Изображение',
                             widget=forms.ClearableFileInput(
                                 attrs={
                                     'class': 'form-control-lg',
                                     'placeholder': 'Изображение',
                                 }
                             ))
    title = forms.CharField(
        label='Название',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Название',
                'class': 'form-control',
                'id': 'floatingInput',
            }
        ))

    class Meta:
        model = Image
        fields = ('title', 'image', 'tags_')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance:
            tags = instance.tags.values_list('name', flat=True)
            self.fields['tags_'].initial = ' '.join(tags)


            # tags = ''
            # for tag in instance.tags.all():
            #     if tags:
            #         tags += ' '
            #     tags += tag.name
            # self.fields['tags_'].initial = tags


class SearchForm(forms.Form):
    query = forms.CharField(
        # label=False,
        label='Поиск',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Поиск по тегу',
                'class': 'form-control form-control-lg',
                'id': 'floatingInput',
            }
        )
    )

# class EditForm(forms.Form):
#     query = forms.CharField(
#         label='Изменить',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'id': 'floatingInput',
                                          'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}))
    password1 = forms.CharField(label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Повтор пароля'}))
    captcha = CaptchaField(label='', widget=CaptchaTextInput(attrs={'class': 'text-uppercase',
                                                                    'placeholder': 'Captcha',
                                                                    'id': 'floatingInput'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widget = {
                'username': forms.TextInput(attrs={'class': 'form-control'}),
                'email': forms.TextInput(attrs={'class': 'form-control'}),
                'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
                'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'id': 'floatingInput',
                                                             'placeholder': 'Логин'}))
    # email = forms.CharField(label='Email',
    #                         widget=forms.TextInput(attrs={'class': 'form-control',
    #                                                        'id': 'floatingInput',
    #                                                        'placeholder': 'Email'}))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'id': 'floatingPassword',
                                                                 'placeholder': 'Пароль'}))


class ContactForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=255,
                                 widget=forms.TextInput(attrs={'class': 'form-control',
                                                               'id': 'floatingInput',
                                                               'placeholder': 'Имя'}))
    email = forms.EmailField(label='Email',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}))
    message = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'class': 'form-control',
                                                           'cols': 60, 'rows': 10,
                                                           'style': 'height: 182px;'}))
    captcha = CaptchaField(label='', widget=CaptchaTextInput(attrs={'class': 'text-uppercase',
                                                                    'placeholder': 'Captcha',
                                                                    'id': 'floatingInput'}))
