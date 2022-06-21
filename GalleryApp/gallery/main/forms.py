from django import forms
from .models import *


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'image', 'tags')


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ('name',)
