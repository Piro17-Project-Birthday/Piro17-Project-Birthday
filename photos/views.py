from django.shortcuts import redirect, render, get_object_or_404

from .forms import PhotoCreateForm
from .models import Photo
from .models import PhotoPage
from posts.models import BirthdayPage
from tmies.models import TmiPage

def photoHome(request, year, pk):
    photo_page = get_object_or_404(PhotoPage, year=year, pk=pk)
    photos = photo_page.photo_set.all()

    bp_owner = get_object_or_404(BirthdayPage, year=year ,pk=pk)
    name = bp_owner.owner.username
    
    if request.user == bp_owner.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0
    
    target_birth = get_object_or_404(BirthdayPage, year=year, pk=pk)
    target_photo = get_object_or_404(PhotoPage, year=year, pk=pk)
    target_tmi = get_object_or_404(TmiPage, year=year, pk=pk) #하단 메뉴용 타겟들

    context = {
        "photos" : photos,
        "pk" : pk,
        "name": name,
        "is_owner": is_owner,
        "year": year,
        "photo_page": photo_page,
        "target_birth" : target_birth,
        "target_photo" : target_photo,
        "target_tmi" : target_tmi,
    }

    return render(request, "photos/photo_home.html", context=context)


def photoCreate(request, year, pk):
    photo_page = get_object_or_404(PhotoPage, year=year, pk=pk)
    form = PhotoCreateForm(request.POST, request.FILES)
    if request.method == "POST":

        if form.is_valid():
            photo = form.save(commit=False)
            photo.receiver = photo_page
            if request.user.is_authenticated :
                photo.photo_uploader = request.user
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