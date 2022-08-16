from django.shortcuts import redirect, render, get_object_or_404

from .forms import PhotoCreateForm
from .models import Photo
from .models import PhotoPage
from posts.models import BirthdayPage

def photoHome(request, year, pk):
    photo_page = get_object_or_404(PhotoPage, year=year, pk=pk)
    photos = photo_page.photo_set.all()

    bp_owner = get_object_or_404(BirthdayPage, year=year ,pk=pk)
    name = bp_owner.owner.full_name
    
    if request.user == bp_owner.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0

    context = {
        "photos" : photos,
        "pk" : pk,
        "name": name,
        "is_owner": is_owner,
        "year": year,
        "photo_page": photo_page,
    }

    return render(request, "photos/photo_home.html", context=context)


def photoCreate(request, year, pk):
    photo_page = get_object_or_404(PhotoPage, year=year, pk=pk)
    form = PhotoCreateForm(request.POST, request.FILES)
    if request.method == "POST":
        
        if form.is_valid():
            print('form valid')
            photo = form.save(commit=False)
            photo.receiver = photo_page
            photo.save()
            return redirect(f"/{photo_page.year}/{photo_page.photo_origin.id}/photo")
    context = {
        'photo_page' : photo_page,
        'form' : form,
    }
    return render(request, template_name='photos/photo_create.html', context=context)

def photoDelete(reqeust, pk):
    photo = Photo.objects.get(pk=pk)
    photo_page = photo.receiver
    photo.delete()
    return redirect(f"/{photo_page.year}/{photo_page.photo_origin.id}/photo")