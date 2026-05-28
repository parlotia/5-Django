"""
URL configuration for day04site project.
"""
from django.contrib import admin
from django.urls import path
from qyt_device.views.add_device import add_device
from qyt_device.views.auth_views import user_login, user_logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add_device', add_device, name='add_device'),
    path('accounts/login', user_login, name='login'),
    path('accounts/login/', user_login, name='login_slash'),
    path('accounts/logout', user_logout, name='logout'),
]
