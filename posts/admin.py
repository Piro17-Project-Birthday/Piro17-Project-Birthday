from django.contrib import admin

#posts.admin.py 

from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass