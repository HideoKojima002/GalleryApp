from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('image_upload/', image_upload, name='image-upload'),
    path('tag_search', tag_search, name='tag-search'),
    path('tag_search_2', tag_search_2, name='tag-search-2'),
    path('delete/<str:img_id>', delete, name='delete'),
    path('image_edit/<str:img_id>', image_edit, name='image-edit'),
    path('picture_page/<str:img_id>', picture_page, name='picture-page'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('about_us/', about_us, name='about-us'),
    path('support/', support, name='support'),
    path('image_upload/', image_upload, name='image-upload'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('by_authors/<int:user_id>', by_authors, name='by-authors'),
    path('like_image/<str:img_id>', like_image, name='like-image'),
]


# class DataMinix:
