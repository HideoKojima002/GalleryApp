from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from .forms import *
from .models import *
from django.db.models import Q


def context_func(form_opt=ImageForm(), search_opt=SearchForm()):
    search_form = search_opt
    img_all = Image.objects.all()
    form = form_opt
    context = {
        'form': form,
        'search_form': search_form,
        'img_all': img_all,
    }
    return context


def image_upload(request):
    form = ImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            image = form.save()
            tags = form.cleaned_data['tags_']
            if tags:
                for tag in tags.split(' '):
                    tag, created = Tag.objects.get_or_create(name=tag)
                    image.tags.add(tag)
            return redirect('index')
    else:
        return render(request, 'main/index.html', context_func())


def index(request):
    return render(request, 'main/index.html', context_func())


def delete(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    img.delete()
    return redirect('index')


def image_edit(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    # img = Image.objects.get(id=img_id)
    form = ImageForm(request.POST or None, request.FILES or None, instance=img)   # , request.FILES,
    if form.is_valid():
        image = form.save()
        tags = form.cleaned_data['tags_']
        if tags:
            for tag in tags.split(' '):
                tag, created = Tag.objects.get_or_create(name=tag)
                image.tags.add(tag)
        return redirect('index')
    context = {
        'form': form,
        'img': img,
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


def picture_page(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    return render(request, 'main/picture_page.html', {'img': img})
