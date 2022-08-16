from django.shortcuts import render, redirect, get_object_or_404
from .models import TmiPage, TmiMessage
from .forms import TmiMessageForm
from posts.models import BirthdayPage

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def detailTmiPage(request,year, pk):
    tmi_page = get_object_or_404(TmiPage, year=year, pk=pk)
    tmi_messages = tmi_page.tmimessage_set.all()
    
    birthday_page = get_object_or_404(BirthdayPage, pk=pk)
    name = birthday_page.owner.full_name
    
    if request.user == birthday_page.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0
    
    context = {
        "tmi_messages": tmi_messages,
        "pk": pk,
        "name": name,
        "is_owner": is_owner,
        "year": year,
        "tmi_page": tmi_page,
    }
    
    return render(request, template_name="tmies/detail_tmi_page.html", context=context)

def createTmiMessage(request, year, pk):
    tmi_page = get_object_or_404(TmiPage, year=year, pk=pk)
    form = TmiMessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            tmi = form.save(commit=False)
            tmi.receiver = tmi_page
            if request.user.is_authenticated :
                tmi.writer = request.user
            tmi.save()
            return redirect(f"/{tmi_page.year}/{tmi_page.tmi_origin.id}/tmi")
    context = {
        'tmi_page': tmi_page,
        'form':form,
        }
    return render(request, template_name='tmies/create_tmi_message.html', context=context)

def deleteTmiMessage(reqeust, pk):
    tmi_message = TmiMessage.objects.get(pk=pk)
    tmi_page = tmi_message.receiver
    tmi_message.delete()
    return redirect(f"/{tmi_page.year}/{tmi_page.tmi_origin.id}/tmi")




@csrf_exempt
def like_ajax(request):
    req = json.loads(request.body)     
    tmi_message_id = req['id']

    message = TmiMessage.objects.get(id=tmi_message_id)
    
    message.like += 1

    message.save()

    return JsonResponse({'id': tmi_message_id})
    