from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    tags_ = forms.CharField(label='Тэги', required=False)

    class Meta:
        model = Image
        fields = ('title', 'image', 'tags_')


class SearchForm(forms.Form):
    query = forms.CharField(
        label='Поиск',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
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