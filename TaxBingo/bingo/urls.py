from django.urls import path
from . import views

app_name = 'bingo'
urlpatterns = [
    path('do_login/', views.do_login, name='do_login'),
    path('do_logout/', views.do_logout, name='do_logout'),
    path('do_force_update/', views.do_force_update, name='do_force_update'),
    path('about/', views.about, name='about'),
    path('', views.index, name='index') 
]