from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('login/',views.MyLoginView.as_view(),name='account_login'),
    path('users/', views.manage_users, name='manage_users'),

]