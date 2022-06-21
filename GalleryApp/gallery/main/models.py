from django.db import models


# class Image(models.Model):
#     title = models.CharField('Название', max_length=200)
#     image = models.ImageField(upload_to='images')
#     tags = models.CharField('Тег', max_length=150)
#
#     def __str__(self):
#         return self.title


class Image(models.Model):
    title = models.CharField('Название', max_length=200)
    image = models.ImageField(upload_to='images')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField('Название', max_length=200)

    def __str__(self):
        return self.name
