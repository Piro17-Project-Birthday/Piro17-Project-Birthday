from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "photos"

urlpatterns = [
    path("<int:year>/<uuid:pk>/photo/", views.photoHome, name="photo_home"),
    path("<int:year>/<uuid:pk>/photo/write", views.photoCreate, name="photo_create"),
    path("<int:pk>/photo/delete/", views.photoDelete, name="photo_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)