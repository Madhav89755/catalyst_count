from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/',include('user_auth_manage.urls')), # for the authentication purposes routes
    path('',include('dashboard.urls')), # for the dashboard pages routes
]
