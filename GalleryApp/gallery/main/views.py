from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from .models import *
from django.db.models import Q


def image_upload(request):
    form = ImageForm(request.POST, request.FILES)
    form_tag = TagForm(request.POST)
    if request.method == 'POST':
        img_all = Image.objects.all()
        if form.is_valid():
            form.save()
            img_obj = form.instance
            return render(request, 'main/index.html', {'form': form, 'img_obj': img_obj, 'img_all': img_all})
    else:
        form = ImageForm()
    return render(request, 'main/index.html', {'form': form})


def index(request):
    form = ImageForm()
    img_all = Image.objects.all()
    return render(request, 'main/index.html', {'form': form, 'img_all': img_all})


def delete(request, img_id):
    img = get_object_or_404(Image, id=img_id)
    img.delete()
    return redirect('index')


def tag_search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', False)
        if searched:
            tags = searched.split(' ')
            query = Q()
            for tag in tags:
                query |= Q(name=tag)
            # images_by_tag = Tag.objects.filter(query)
            images_by_tag = Image.objects.filter(query)
        context = {'searched': searched, 'tag': images_by_tag}
        return render(request, 'main/tag_search.html', context)
