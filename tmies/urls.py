from django.urls import path 
from . import views

app_name = "tmies"

urlpatterns = [
    path('tmi/<int:pk>', views.detailTmiPage, name='detail_tmi_page'),
    path('tmi/<int:pk>/write/', views.createTmiMessage, name='create_tmi_message'),
    path('tmi/<int:pk>/delete/', views.deleteTmiMessage, name='delete_tmi_message'),
    path('like_ajax/', views.like_ajax, name ='like_ajax'),
    
]