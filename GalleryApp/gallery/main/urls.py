from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('image_upload', image_upload, name='image-upload'),
    path('tag_search', tag_search, name='tag-search'),
    path('delete/<int:img_id>', delete, name='delete'),
]
