from django.shortcuts import render, redirect, get_object_or_404

from datetime import date, datetime, timedelta
from users.models import User
from .models import BirthdayPage
from .models import Message
from photos.models import PhotoPage
from .forms import MessageForm, LoginedMessageForm, BirthdayPageForm
from .forms import MessageForm, BirthdayPageForm, EditMyPageForm
from tmies.models import TmiPage
import random

#도메인 년도 비교용 전역변수
today = datetime.now().date() #현재 날짜
today_year = today.year #현재 년도
next_year = today_year + 1

def main(request):
    if request.user.is_authenticated: #로그인 한 사용자라면 
        #birthday page가 이미 만들어졌다면
        if BirthdayPage.objects.filter(owner=request.user, year=next_year).exists() : #birthday page가 올해 page라면
            current_birthday_page = BirthdayPage.objects.get(owner=request.user, year=next_year)
            return redirect(f"{current_birthday_page.year}/{current_birthday_page.id}") #해당 페이지로 이동한다
        elif BirthdayPage.objects.filter(owner=request.user, year=today_year).exists():       #birthday page가 내년 page라면 (올해 생일이 이미 지났다면)
            current_birthday_page = BirthdayPage.objects.get(owner=request.user, year=today_year)
            return redirect(f"{current_birthday_page.year}/{current_birthday_page.id}")
    return render(request, "posts/main.html")

def createBirthdayPage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = BirthdayPageForm(request.POST)
            if form.is_valid():
                #현재 로그인 한 유저를 owner로 하는 birthday page 생성
                birthday_page = BirthdayPage.objects.create(owner=request.user)
                #form에 입력한 정보대로 owner의 full name과 birthday 수정 후 저장
                birthday_page.owner.username = form.cleaned_data['username']
                birthday_page.owner.birthday = form.cleaned_data['birthday']
                birthday_page.owner.selected_cake = form.cleaned_data['selected_cake']
                birthday_page.owner.save()
                
                tmi_page = TmiPage.objects.create(tmi_origin=birthday_page)
                photo_page = PhotoPage.objects.create(photo_origin=birthday_page)
                
                #페이지에 입력된 생일을 받아서 올해 생일이 지났는지 판별
                birthday_month = birthday_page.owner.birthday.month
                birthday_day = birthday_page.owner.birthday.day
                birthday_thisyear = datetime.strptime(str(today_year)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #올해 생일
                
                birthday = birthday_thisyear #생일은 올해 생일로 초기화한다
                date_diff = abs((today-birthday).days)
                
                if birthday_thisyear < today: #올해 생일이 이미 지났다면 내년 생일 페이지를 미리 생성해 줌
                    page_year = today_year + 1
                    birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
                    date_diff = abs((today-birthday).days)
                    
                    if date_diff < 7:
                        tmi_page.state = "activate"
                        photo_page.state = "activate"
                        birthday_page.state = "upcoming"
                    elif date_diff == 7:
                        tmi_page.state = "activate"
                        photo_page.state = "activate"
                        birthday_page.state = "today"
                    else:
                        tmi_page.state = "deactivate"
                        photo_page.state = "deactivate"
                        birthday_page.state = "waiting"
                else:                         #올해 생일이 아직 지나지 않았다면 올해 생일 페이지가 생성됨
                    page_year = today_year
                    if date_diff < 7:
                        tmi_page.state = "activate"
                        photo_page.state = "activate"
                        birthday_page.state = "upcoming"
                    elif date_diff ==7:
                        tmi_page.state = "activate"
                        photo_page.state = "activate"
                        birthday_page.state = "today"
                    else:
                        tmi_page.state = "deactivate"
                        photo_page.state = "deactivate"
                        birthday_page.state = "waiting"
                    
                birthday_page.year = page_year
                birthday_page.save()
                
                tmi_page.year = page_year
                photo_page.year = page_year
                tmi_page.save()
                photo_page.save()
                
                #만들어진 페이지로 redirect
                return redirect(f"{birthday_page.year}/{birthday_page.id}")
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
    
def detailBirthdayPage(request,year,pk):
    birthday_page = get_object_or_404(BirthdayPage, year=year, pk=pk)
    messages = birthday_page.message_set.all()
    name = birthday_page.owner.username
    
    print(datetime.now())
    if request.user == birthday_page.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0

    birthday_month = birthday_page.owner.birthday.month #생일자의 생일 월
    birthday_day = birthday_page.owner.birthday.day #생일자의 생일 일
    # today = datetime.now().date() #현재 날짜
    # today_year = today.year #현재 년도

    birthday_thisyear = datetime.strptime(str(today_year)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #올해 생일
    birthday = birthday_thisyear #생일은 올해 생일로 초기화한다
    date_diff = abs((today-birthday).days) 
    
    # if birthday_thisyear < today : #올해 생일이 이미 지났다면
    #     birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
    #     date_diff = abs((today-birthday).days)
    #     if date_diff <= 7: #생일이 7일 이내로 남았다면
    #         birthday_state = "upcoming"
    #     else :
    #         birthday_state = "waiting" 
    # else : #올해 생일이 아직 오지 않았다면
    #     if date_diff == 0 : #생일이 오늘이라면
    #         birthday_state = "today"
    #     elif date_diff <= 7: #생일이 7일 이내로 남았다면
    #         birthday_state = "upcoming"
    #     else : #생일이 7일 넘게 남았다면
    #         birthday_state = "waiting"
        
    #생일이 자정이 지나 끝나면 비활성화
    print(birthday_thisyear)
    print(today)
    print(birthday_thisyear >= today)
    if birthday_thisyear >= today :
        curr_page = birthday_page
        tmi_page = TmiPage.objects.get(tmi_origin=curr_page)
        photo_page = PhotoPage.objects.get(photo_origin=curr_page)
        if date_diff == 0:
            curr_page.state = 'today'
            tmi_page.state = 'activate'
            photo_page.state = 'activate'
        elif date_diff <=7:
            curr_page.state = "upcoming"
            tmi_page.state = 'activate'
            photo_page.state = 'activate'
        else:
            curr_page.state = "waiting"
            tmi_page.state = 'deactivate'
            photo_page.state = 'deactivate'
        curr_page.save()
        tmi_page.save()
        photo_page.save()
    else:
        if is_owner == 1:
            if BirthdayPage.objects.filter(owner=request.user, year=today_year).exists():    
                birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
                date_diff = abs((today-birthday).days)
                if not BirthdayPage.objects.filter(owner=request.user, year=next_year).exists():
                    curr_page = BirthdayPage.objects.get(owner=request.user, year=today_year)
                                
                    next_page = BirthdayPage.objects.create(owner=request.user, year=next_year)
                    next_name = curr_page.owner.username
                    next_birth = curr_page.owner.birthday
                    next_cake = curr_page.owner.selected_cake
                                
                    next_page.owner.username= next_name
                    next_page.owner.birthday = next_birth
                    next_page.owner.selected_cake = next_cake
                    next_page.owner.save()
                    
                    tmi_page = TmiPage.objects.create(tmi_origin = next_page, year= next_page.year)
                    photo_page = PhotoPage.objects.create(photo_origin = next_page, year= next_page.year)
                        
                    if date_diff <=7:
                        next_page.state = "upcoming"
                        tmi_page.state = "activate"
                        photo_page.state = "activate"
                        print(next_page.state,1)
                        print(tmi_page.state,1)
                        print(photo_page.state,1)
                    else:
                        next_page.state = "waiting"
                        tmi_page.state = "deactivate"
                        photo_page.state = "deactivate"
                        print(next_page.state,2)
                        print(tmi_page.state,2)
                        print(photo_page.state,2)
                        
                    next_page.save()
                    tmi_page.save()
                    photo_page.save()
                    
                    print(3)
                    print(3)
                    print(3)
                        
                    
                    curr_page.state = "archive"
                    curr_page.save()
                else:
                    curr_page = BirthdayPage.objects.get(owner=request.user, year=today_year)
                    curr_page.state = "archive"
                    curr_page.save()
                    
                    tmi_page = TmiPage.objects.get(tmi_origin=curr_page)
                    photo_page = PhotoPage.objects.get(photo_origin=curr_page)
                    
                    tmi_page.state = "archive"
                    photo_page.state = "archive"
                    
                    tmi_page.save()
                    photo_page.save()
                    
            else:
                birthday = datetime.strptime(str(today_year+1)+str(birthday_month)+str(birthday_day), "%Y%m%d").date() #생일을 내년 생일로 한다
                date_diff = abs((today-birthday).days)
                curr_page = birthday_page
                if date_diff == 0:
                    curr_page.state = 'today'
                elif date_diff <=7:
                    curr_page.state = "upcoming"
                else:
                    curr_page.state = "waiting"
                    curr_page.save()
        # print(birthday_page.year)
        # print(birthday_page.id)
        # print(birthday_page.state)
            
# context 전달 다시
        
    selected_cake = birthday_page.owner.selected_cake
    
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
        # "birthday_state" : birthday_state,
        "pk" : pk,
        "is_owner" : is_owner,
        "selected_cake" : selected_cake,
        "target" : target,
        "year": year,
        "birthday_page": birthday_page,
        
    }
    return render(request, template_name="posts/detail_birthday_page.html", context=context)
    
def createMessage(request,year,pk):
    profile_img_1 = "/static/img/icon/cake-candles-solid.svg"
    profile_img_2 = "/static/img/icon/envelope-solid.svg"
    profile_img_3 = "/static/img/icon/gift-solid.svg"
    profile_img_set = [profile_img_1, profile_img_2, profile_img_3]
    profile_img = random.choice(profile_img_set)
    birthday_page = get_object_or_404(BirthdayPage, year=year, pk=pk)
    if request.user.is_authenticated:
        form = LoginedMessageForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.profile_img = profile_img
                post.receiver = birthday_page
                if request.user.is_authenticated :
                    post.sender = request.user
                post.save()
                return redirect(f"/{birthday_page.year}/{birthday_page.id}")
        context = {
            'birthday_page' : birthday_page,
            'form' : form,
            'profile_img' : profile_img
        }
        return render(request, template_name='posts/create_message.html', context=context)
    else :
        form = MessageForm(request.POST)
        if request.method == 'POST':
            if form.is_valid():
                post = form.save(commit=False)
                post.profile_img = random.choice(profile_img_set)
                post.receiver = birthday_page
                if request.user.is_authenticated :
                    post.sender = request.user
                post.save()
                return redirect(f"/{birthday_page.year}/{birthday_page.id}")
        context = {
            'birthday_page' : birthday_page,
            'form' : form,
            'profile_img' : profile_img
        }
        return render(request, template_name='posts/create_message.html', context=context)

def deleteMessage(request, pk):
    message = Message.objects.get(pk=pk)
    birthday_page = message.receiver
    message.delete()
    return redirect(f"/{birthday_page.year}/{birthday_page.id}")

def mainMypage(request):
    if request.user.is_authenticated:
        curr_user = request.user
        target_pages = BirthdayPage.objects.filter(owner=curr_user).order_by('-id')
        archived_pages = BirthdayPage.objects.filter(owner=request.user,state="archive")
            
        context = {
            "curr_user": curr_user,
            "target_pages": target_pages,
            "archived_pages": archived_pages,
        }
        return render(request, 'posts/main_mypage.html', context=context)
    else:
        return redirect("/login")
        
def editMypage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = EditMyPageForm(request.POST)
            if form.is_valid():
                birthday_page = BirthdayPage.objects.get(owner=request.user, year=today_year)

                birthday_page.owner.username = form.cleaned_data['username']
                birthday_page.owner.selected_cake = form.cleaned_data['selected_cake']
                birthday_page.owner.save()
                
                return redirect ('/mypage/main')
            else :
                return redirect('/')
        else:
            form = EditMyPageForm(instance=request.user)
            context={
                'form':form,
            }
            return render(request, 'posts/edit_mypage.html', context=context)
    else :
        return redirect("/login")


# 아래코드 필요없으면 나중에 지울예정 

    
class OriginalInformation():
    
    def remember(self, request, command):
        if 'signup' in command:
            self.email = request.POST['email']
        elif 'password_forgotten' not in command:
            self.current_password = request.POST['current_password']
        self.new_password1 = request.POST['new_password1']
        self.new_password2 = request.POST['new_password2']
        if 'password_forgotten' not in command:
            self.nickname = request.POST['nickname']
            self.birth_y = request.POST['birth-y']
            self.birth_m = request.POST['birth-m']
            self.birth_d = request.POST['birth-d']
            self.img = request.FILES.get('img')
            self.img_setting = request.POST.get('img_setting')
            self.introduction = request.POST['introduction']
            self.job = request.POST.get('job')

# Birth Format (YYYY-MM-DD)


def birth_format(year, month, day):
    today = date.today()
    try:
        if int(year) > today.year:
            return ''
        birth = datetime(int(year), int(month), int(day)).strftime("%Y-%m-%d")
        return birth
    except:  # 잘못된 날짜
        return ''