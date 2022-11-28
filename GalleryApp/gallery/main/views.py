from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, FormView
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

from .forms import *
from .models import *
from django.db.models import Q


def context_func(form_opt=ImageForm(), search_opt=SearchForm()):
    search_form = search_opt
    img_all = Image.objects.all()
    form = form_opt
    # menu = [{'title': "O нас", 'url_name': "about-us"},
    #         {'title': "O нас", 'url_name': "about-us"}
    # ]
    context = {
        'form': form,
        'search_form': search_form,
        'img_all': img_all,
    }

    return context


@login_required(redirect_field_name='my_redirect_field')
def image_upload(request):
    form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            img_user = form.save(commit=False)
            img_user.author = request.user
            img_user.save()
            image = form.save()
            tags = form.cleaned_data['tags_']
            if tags:
                for tag in tags.split(' '):
                    tag, created = Tag.objects.get_or_create(name=tag)
                    image.tags.add(tag)
            return redirect('index')
    else:
        return render(request, 'main/image_upload.html', context_func())


def index(request):
    return render(request, 'main/index.html', context_func())


@login_required(redirect_field_name='my_redirect_field')
def delete(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    img.delete()
    return redirect('index')


# @login_required(redirect_field_name='my_redirect_field')
# def delete(request, img_id):
#     img = get_object_or_404(Image, id=img_id)
#     if img.author != request.user:
#         return 0
#     img.delete()
#     return redirect('index')


@login_required(redirect_field_name='my_redirect_field')
def image_edit(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    # img = Image.objects.get(id=img_id)
    form = ImageForm(request.POST or None, request.FILES or None, instance=img)   # , request.FILES,
    if form.is_valid():
        # image_old = get_object_or_404(Image, id=img_id)
        # old_tags = {tag.name for tag in image_old.tags.all()}
        image = form.save()
        tags = form.cleaned_data['tags_']
        if tags:
            # new_tags = {tag for tag in tags.split(' ')}
            for tag in tags.split(' '):
                tag, created = Tag.objects.get_or_create(name=tag)
                image.tags.add(tag)
            for tag in image.tags.all():
                if tag.name not in tags:
                    image.tags.remove(tag)
        else:
            image.tags.clear()

        return redirect('index')
    context = {
        'form': form,
        'img': img,
        'tags': [tag.name for tag in img.tags.all()]
    }
    return render(request, 'main/image_edit.html', context)


# @require_http_methods(["POST"])
def tag_search(request):
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            searched = search_form.cleaned_data['query']
            tags = searched.split(' ')
            query = Q()
            for tag in tags:
                query |= Q(tags__name=tag)
            images_by_tag = Image.objects.filter(query).distinct()
            context = {'searched': searched,
                       'tag': images_by_tag,
                       }
            return render(request, 'main/tag_search.html', context)
        else:

            return render(request, 'main/index.html', context_func())
    else:
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            searched = search_form.cleaned_data['query']
            tags = searched.split(' ')
            query = Q()
            for tag in tags:
                query |= Q(tags__name=tag)
            images_by_tag = Image.objects.filter(query).distinct()
            context = {'searched': searched,
                       'tag': images_by_tag,
                       }
            return render(request, 'main/tag_search.html', context)
        else:
            return render(request, 'main/index.html', context_func())


# Заведомо неверное решение
# def tag_search(request):
#     if request.method == 'POST':
#         searched = request.POST.get('searched', False)
#         flag_list = searched.split()
#         for item in flag_list:
#             tag = Image.objects.filter(tags__contains=item)
#             context = {'searched': searched,  'tag': tag}
#         return render(request, 'main/tag_search.html', context)


@require_http_methods(["GET"])
def tag_search_2(request):
    searched = request.GET.get('query')
    tags = searched.split(' ')
    query = Q()
    for tag in tags:
        query |= Q(tags__name=tag)
    images_by_tag = Image.objects.filter(query).distinct()
    context = {'searched': searched,
               'tag': images_by_tag,
               }
    return render(request, 'main/tag_search.html', context)


def picture_page(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    form = ImageForm()
    # img_user = img.author
    img_user = request.user.id
    context = {
        # 'img_user': img_user,
        'form': form,
        'img': img,
        'tags': [tag.name for tag in img.tags.all()]
    }
    return render(request, 'main/picture_page.html', context)


def about_us(request):
    return render(request, 'main/about_us.html', context_func())


def support(request):
    return render(request, 'main/support.html', context_func())


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'main/login.html'

    def get_success_url(self):
        return reverse_lazy('index')


class ContactFormView(FormView):
    form_class = ContactForm
    template_name = 'main/contact.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):          # Работа с шаблоном сообщения на почту.
        print(form.cleaned_data)
        subject = f"Communication with the client - {form.cleaned_data['first_name']}"
        body = {
            'first_name': form.cleaned_data['first_name'],
            'email': form.cleaned_data['email'],
            'message': form.cleaned_data['message'],
        }
        message = "\n".join(body.values())
        try:
            send_mail(subject, message,
                      'hideokojima002@gmail.com',
                      ['hideokojima002@gmail.com'])
        except BadHeaderError:
            return HttpResponse('Найден некорректный заголовок')
        return redirect('index')

