from django.urls import path
from . import views

app_name = 'bingo'
urlpatterns = [
    path('do_login/', views.do_login, name='do_login'),
    path('do_logout/', views.do_logout, name='do_logout'),
    path('', views.index, name='index') 
]