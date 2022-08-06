from django.contrib import admin
from .models import Post, BirthdayPage

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(BirthdayPage)
class BirthdayPageAdmin(admin.ModelAdmin):
    pass