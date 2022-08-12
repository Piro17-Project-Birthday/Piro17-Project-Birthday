from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "photos"

urlpatterns = [
    path("photo/<int:pk>", views.photoHome, name="photo_home"),
    path("photo/<int:pk>/photocreate/", views.photoCreate, name="photo_create"),
    path("photo/<int:pk>/photodelete/", views.photoDelete, name="photo_delete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)