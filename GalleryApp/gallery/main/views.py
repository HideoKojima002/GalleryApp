from django.shortcuts import render
from .forms import ImageForm
from .models import Image
from django.db.models import Q


def image_upload(request):
    form = ImageForm(request.POST, request.FILES)
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
    return render(request, 'main/index.html')


def delete(request):
    if request.method == 'POST':
        records = Image.objects.all()
        records.delete()
        return render(request, 'main/index.html')




def tag_search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', False)
        tag = ''
        if searched:
            query = Q()
            for item in searched:
                query |= Q(tags__contains=item)
            tag = Image.objects.filter(query)
        context = {'searched': searched, 'tag': tag}
        return render(request, 'main/tag_search.html', context)




