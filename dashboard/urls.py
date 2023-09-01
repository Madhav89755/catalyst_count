from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.upload_data, name='dashboard'),
    path('query_builder/', views.query_builder, name='query_builder'),
    path('query_api/', views.query_api, name='query_api'),
]