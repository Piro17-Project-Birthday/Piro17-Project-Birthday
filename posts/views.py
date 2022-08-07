from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import BirthdayPage
from .models import Post
from .forms import PostForm, BirthdayPageForm

def createBirthdayPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BirthdayPageForm(request.POST)
            if form.is_valid():
                #현재 로그인 한 유저를 owner로 하는 birthday page 생성
                birthday_page = BirthdayPage.objects.create(owner=request.user)
                #form에 입력한 정보대로 owner의 full name과 birthday 수정 후 저장
                birthday_page.owner.full_name = form.cleaned_data['full_name']
                birthday_page.owner.birthday = form.cleaned_data['birthday']
                birthday_page.owner.save()
                #만들어진 페이지로 redirect
                return redirect(f"/{birthday_page.id}")
            else :
                return redirect('/')
        else :
            form = BirthdayPageForm(request.POST)
            context={
                'form':form,
            }
            return render(request, 'posts/create_birthday_page.html', context=context)
    else :
        return redirect("/login")
    
def detailBirthdayPage(request,pk):
    birthday_page = BirthdayPage.objects.get(pk=pk)
    name = birthday_page.owner.full_name

    birthday_month = birthday_page.owner.birthday.month #생일자의 생일 월
    birthday_day = birthday_page.owner.birthday.day #생일자의 생일 일
    today = datetime.now().date() #현재 날짜
    today_year = today.year #현재 년도

    birthday_thisyear = datetime.strptime(str(today_year)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #올해 생일
    birthday = birthday_thisyear #생일은 올해 생일로 초기화한다
    date_diff = abs((today-birthday).days) 
    if birthday_thisyear < today : #올해 생일이 이미 지났다면
        birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
        birthday_state = "passed"
        date_diff = abs((today-birthday).days) 
    else : #올해 생일이 아직 오지 않았다면
        if date_diff == 0 : #생일이 오늘이라면
            birthday_state = "today"
        elif date_diff <= 7: #생일이 7일 이내로 남았다면
            birthday_state = "upcoming"
        else : #생일이 7일 넘게 남았다면
            birthday_state = "waiting"
        
    context = {
        "name" : name,
        "birthday" : birthday,
        "date_diff" : date_diff,
        "birthday_state" : birthday_state
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