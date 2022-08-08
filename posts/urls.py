from django.urls import path 
from . import views
from django.conf import settings
from django.views.generic.base import TemplateView
from django.conf.urls.static import static

app_name = "posts"

urlpatterns = [
    path('', views.home, name="home"),
    path('', TemplateView.as_view(template_name = 'home.html'), name = 'home'),
] 