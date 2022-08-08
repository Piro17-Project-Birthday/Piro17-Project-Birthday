from django.contrib import admin
from .models import Message, BirthdayPage

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    pass

@admin.register(BirthdayPage)
class BirthdayPageAdmin(admin.ModelAdmin):
    pass