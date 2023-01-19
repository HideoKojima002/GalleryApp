import uuid

from django.contrib.auth.models import User
from django.db import models


# class Image(models.Model):
#     title = models.CharField('Название', max_length=200)
#     image = models.ImageField(upload_to='images')
#     tags = models.CharField('Тег', max_length=150)
#
#     def __str__(self):
#         return self.title


class Image(models.Model):
    # index_img = models.BigAutoField(auto_created=True, primary_key=False, serialize=False)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField('Название', max_length=200)
    image = models.ImageField(upload_to='images')
    tags = models.ManyToManyField('Tag')
    author = models.ForeignKey(User, related_name='author', on_delete=models.CASCADE)
    date_img = models.DateField(auto_now_add=True)
    time_img = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)     # Можно попробовать это Field.unique для уникальности

    def __str__(self):
        return self.name
