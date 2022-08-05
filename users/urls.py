# users/urls.py 
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "users"

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.LoginView.as_view(), name="log_in"),
    path("logout/", views.log_out, name="log_out"),
    path("signup/", views.sign_up, name="sign_up"),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 