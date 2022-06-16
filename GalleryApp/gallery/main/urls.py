from django.urls import path
from . import views

urlpatterns = [
    path('', views.image_upload),
    path(' tag_search ', views.tag_search, name='tag-search'),
    path(' delete ', views.delete, name='Delete'),
]