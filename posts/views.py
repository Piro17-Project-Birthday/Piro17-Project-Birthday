from django.shortcuts import render, redirect, get_object_or_404

from datetime import date, datetime, timedelta
from users.models import User
from .models import BirthdayPage
from .models import Message
from photos.models import PhotoPage
from .forms import MessageForm, LoginedMessageForm, BirthdayPageForm

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
    
    if request.user == birthday_page.owner :
        is_owner = 1 #현재 접속자가 이 생일 페이지의 주인인지 알려주는 플래그
    else :
        is_owner = 0
        
    selected_cake = birthday_page.owner.selected_cake
    
    if selected_cake == "초코 케이크":
        target = "초코"
    elif selected_cake == "딸기 케이크":
        target = "딸기"
    elif selected_cake == "치즈 케이크":
        target = "치즈"
    # ##############################################################
    # my_messages = Message.objects.filter(sender=request.user)
    # print(my_messages)
   
     
            
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
        # "my_messages":my_messages,
        
    }
    return render(request, template_name="posts/detail_birthday_page.html", context=context)
    
def createMessage(request, pk):
    birthday_page = get_object_or_404(BirthdayPage, pk=pk)
    if request.user.is_authenticated:
        form = LoginedMessageForm(request.POST)
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
    else :
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