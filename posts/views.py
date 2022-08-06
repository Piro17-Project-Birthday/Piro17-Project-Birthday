from django.shortcuts import render, redirect
from .models import BirthdayPage

def createBirthdayPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            BirthdayPage.objects.create(owner=request.user)
            return redirect("/")
    
        context={
            "request_user" : request.user
        }
        return render(request, template_name ="posts/create_birthday_page.html", context=context)
    else :
        return redirect("/login")
    
def detailBirthdayPage(request,pk):
    birthdayPage = BirthdayPage.objects.get(pk=pk)
    context = {
        "birthdayPage" : birthdayPage
    }
    return render(request, template_name="posts/detail_birthday_page.html", context=context)