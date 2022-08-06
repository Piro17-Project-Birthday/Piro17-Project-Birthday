from django.shortcuts import render, redirect, get_object_or_404
from .models import BirthdayPage
from .models import Post
from .forms import PostForm

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
    
# def msgWrite(request):
#     if request.method == 'POST':
#         nickname = request.POST['nickname']
#         message = request.POST['message']
#         is_private = request.POST.get('is_private', False)
        
#         Post.objects.create(nickname=nickname, message=message, is_private=is_private)
        
#         return redirect('/')
#     return render(request, template_name='posts/write.html')

def msgWrite(request, pk):
    birthdayPage = get_object_or_404(BirthdayPage, pk=pk)
    form = PostForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.receiver = birthdayPage
            if request.user.is_authenticated :
                post.sender = request.user
            post.save()
    context = {
        'birthdayPage' : birthdayPage,
        'form' : form
    }
    return render(request, template_name='posts/write.html', context=context)