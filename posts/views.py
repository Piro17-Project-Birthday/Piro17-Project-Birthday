from django.shortcuts import render, redirect
from .models import BirthdayPage
from .models import Post

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
    
def msgWrite(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        message = request.POST['message']
        is_private = request.POST.get('is_private', False)
        
        Post.objects.create(nickname=nickname, message=message, is_private=is_private)
        
        return redirect('/')
    return render(request, template_name='posts/write.html')