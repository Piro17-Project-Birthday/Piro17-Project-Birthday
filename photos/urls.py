from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.conf.urls import url

app_name = "photos"

urlpatterns = [
    path("<int:year>/<uuid:pk>/photo/", views.photoHome, name="photo_home"),
    path("<int:year>/<uuid:pk>/photo/write", views.photoCreate, name="photo_create"),
    path("<int:pk>/photo/delete/", views.photoDelete, name="photo_delete"),
] + url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})