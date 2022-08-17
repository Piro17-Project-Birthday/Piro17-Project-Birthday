from django.contrib import admin
from .models import TmiPage, TmiMessage

@admin.register(TmiMessage)
class TmiMessageAdmin(admin.ModelAdmin):
    pass

@admin.register(TmiPage)
class TmiPageAdmin(admin.ModelAdmin):
    pass