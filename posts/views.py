from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime

from users.models import User
from .models import BirthdayPage
from .models import Message
from .forms import MessageForm, BirthdayPageForm

def main(request):
    if request.user.is_authenticated: #로그인 한 사용자라면
        if BirthdayPage.objects.filter(owner=request.user).exists() : #birthday page가 이미 만들어졌다면
            return redirect(f"/{BirthdayPage.objects.get(owner=request.user).id}") #해당 페이지로 이동한다
    return render(request, "posts/main.html")

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
                birthday_page.owner.selected_cake = form.cleaned_data['selected_cake']

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
    birthday_page = get_object_or_404(BirthdayPage, pk=pk)
    messages = birthday_page.message_set.all()
    name = birthday_page.owner.full_name

    birthday_month = birthday_page.owner.birthday.month #생일자의 생일 월
    birthday_day = birthday_page.owner.birthday.day #생일자의 생일 일
    today = datetime.now().date() #현재 날짜
    today_year = today.year #현재 년도

    # Arrow Library 쓰는 것을 강력히 권고드립니다.
    # https://arrow.readthedocs.io/en/latest/
    # now = arrow.Arrow.now()
    # birthday_this_year = arrow.Arrow.strptime("2022-08-10", "%Y-%m-%d")
    # birthday_this_year = now.replace(year=2022, month=8, day=10, hour=0, second=0, minute=0)
    # now.day
    # now.month

    birthday_thisyear = datetime.strptime(str(today_year)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #올해 생일
    birthday = birthday_thisyear #생일은 올해 생일로 초기화한다
    date_diff = abs((today-birthday).days)
    if birthday_thisyear < today : #올해 생일이 이미 지났다면
        birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
        date_diff = abs((today-birthday).days)
        if date_diff <= 7: #생일이 7일 이내로 남았다면
            birthday_state = "upcoming"
        else :
            birthday_state = "waiting"
    else : #올해 생일이 아직 오지 않았다면
        if date_diff == 0 : #생일이 오늘이라면
            birthday_state = "today"
        elif date_diff <= 7: #생일이 7일 이내로 남았다면
            birthday_state = "upcoming"
        else : #생일이 7일 넘게 남았다면
            birthday_state = "waiting"

    # 아래로 대체 가능
    # is_owner = request.user == birthday_page.owner
    if request.user == birthday_page.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0

    selected_cake = birthday_page.owner.selected_cake

    # "크림치즈 케이크"가 들어오면 target은 정의가 안됨
    # 아래와 같이 dict 활용 권장
    # cake_target_mapping = {
    #     "초코 케이크": "초코",
    #     "딸기 케이크": "딸기"
    # }
    # target = cake_target_mapping.get(selected_cake, "이상한 케이크")
    # =======================
    # 셀렉티드 케이크가 모델에 Choice Field로 정의되어 있으면,
    # 여기서 분기 처리를 해주면 나중에 새로운 케이크 추가할 때 에러 발생 확률 높아짐
    # cake_target_mapping을 모델에 정의하고 임포트해서 써야 함.
    if selected_cake == "초코 케이크":
        target = "초코"
    elif selected_cake == "딸기 케이크":
        target = "딸기"
    elif selected_cake == "치즈 케이크":
        target = "치즈"

    context = {
        "messages" : messages,
        "name" : name,
        "birthday" : birthday,
        "date_diff" : date_diff,
        "birthday_state" : birthday_state,
        "pk" : pk,
        "is_owner" : is_owner,
        "selected_cake" : selected_cake,
        "target" : target,
    }
    return render(request, template_name="posts/detail_birthday_page.html", context=context)

def createMessage(request, pk):
    birthday_page = get_object_or_404(BirthdayPage, pk=pk)
    form = MessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            post = form.save(commit=False)
            post.receiver = birthday_page
            if request.user.is_authenticated :
                post.sender = request.user
            post.save()
            return redirect(f"/{birthday_page.id}")
    context = {
        'birthday_page' : birthday_page,
        'form' : form
    }
    return render(request, template_name='posts/create_message.html', context=context)

def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)
    birthday_page = message.receiver
    message.delete()
    return redirect(f"/{birthday_page.id}")

def mypage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            form = BirthdayPageForm(request.POST)
            if form.is_valid():
                birthday_page = BirthdayPage.objects.get(owner=request.user)

                # KeyError 발생할 수 있어 .get 권장
                birthday_page.owner.full_name = form.cleaned_data['full_name']
                birthday_page.owner.birthday = form.cleaned_data['birthday']
                birthday_page.owner.selected_cake = form.cleaned_data['selected_cake']

                birthday_page.owner.save()

                return redirect(f"/{birthday_page.id}")
            else :
                return redirect('/')
        else:
            form = BirthdayPageForm(instance=request.user)
            context={
                'form':form,
            }
            return render(request, 'posts/mypage.html', context=context)
    else :
        return redirect("/login")
