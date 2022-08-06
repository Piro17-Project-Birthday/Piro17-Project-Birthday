from django.urls import path 

from . import views

app_name = "posts"

urlpatterns = [
    path('create', views.createBirthdayPage, name='create_birthday_page'),
    path('<int:pk>', views.detailBirthdayPage, name="detail_birthday_page"),
    path('<int:pk>/write/', views.msgWrite, name='write'),
]