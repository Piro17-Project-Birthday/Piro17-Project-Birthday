from django.urls import path 

from . import views

app_name = "posts"

urlpatterns = [
    path('write', views.msgWrite, name="write"),
    path('', views.testHome, name="testHome"),
]