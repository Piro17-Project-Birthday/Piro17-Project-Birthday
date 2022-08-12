from django.contrib import admin
from .models import PhotoPage, Photo

@admin.register(PhotoPage)
class PhotoPageAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass