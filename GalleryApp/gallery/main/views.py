from django.shortcuts import render
from .forms import ImageForm
from .models import Image


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


def searach(request):
    pass