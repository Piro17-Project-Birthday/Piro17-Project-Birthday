from django.urls import path 
from . import views

app_name = "tmies"

urlpatterns = [
    path('<int:year>/<int:pk>/tmi/', views.detailTmiPage, name='detail_tmi_page'),
    path('<int:year>/<int:pk>/tmi/write/', views.createTmiMessage, name='create_tmi_message'),
    path('<int:pk>/tmi/delete/', views.deleteTmiMessage, name='delete_tmi_message'),
    path('like_ajax/', views.like_ajax, name ='like_ajax'),
    
]