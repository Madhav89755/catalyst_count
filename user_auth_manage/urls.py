from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',views.loginView,name='login_page'),
    path('users/', views.manage_users, name='manage_users'),

]