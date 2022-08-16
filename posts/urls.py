from django.urls import path 
from . import views
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

app_name = "posts"

urlpatterns = [
    path("", views.main, name="main"),
    path('create', views.createBirthdayPage, name='create_birthday_page'),
    path('<int:year>/<int:pk>', views.detailBirthdayPage, name="detail_birthday_page"),
    path('<int:year>/<int:pk>/write/', views.createMessage, name='create_message'),
    path('<int:pk>/delete/', views.deleteMessage, name='delete_message'),
    path('mypage/main',views.mainMypage, name='main_mypage'),
    path('mypage/edit', views.editMypage, name= "edit_mypage"),
]