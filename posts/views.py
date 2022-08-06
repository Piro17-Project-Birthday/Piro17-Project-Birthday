from django.shortcuts import redirect, render
from .models import Post

def msgWrite(request):
    if request.method == 'POST':
        nickname = request.POST['nickname']
        message = request.POST['message']
        is_private = request.POST.get('is_private', False)
        
        Post.objects.create(nickname=nickname, message=message, is_private=is_private)
        
        return redirect('/')
    return render(request, template_name='posts/write.html')

def testHome(request):
    posts = Post.objects.all()
    context = {
        "posts" : posts
    }
    return render(request, template_name='posts/testHome.html', context = context)