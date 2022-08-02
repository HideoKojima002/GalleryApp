from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    tags_ = forms.CharField(label='Тэги', required=False)

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
        label='Поиск',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Поиск по тегу',
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
