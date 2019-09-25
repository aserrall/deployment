from django.contrib.auth import logout, login
from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'register/', views.register, name='register'),
    path(r'accounts/login/', login, name='login'),
    path(r'accounts/logout/', logout, {'next_page': '/'}, name='logout'),

    path(r'foro/', views.forum, name='forum'),

    ]
