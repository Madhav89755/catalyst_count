from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('auth/',include('user_auth_manage.urls')), # for the authentication purposes routes
    path('',include('dashboard.urls')), # for the dashboard pages routes
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)