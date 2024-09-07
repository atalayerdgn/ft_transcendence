"""
URL configuration for transandancefirst project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from transandancefirst.usermanagment.views.views import UserManagementHandler

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserManagementHandler.as_view({'get': 'list_users'}), name='list_users'),
    path('users/id/', UserManagementHandler.as_view({'get': 'get_user_by_id'}), name='get_user_by_id'),
    path('users/username/', UserManagementHandler.as_view({'get': 'get_user_by_username'}), name='get_user_by_username'),
    path('users/email/', UserManagementHandler.as_view({'get': 'get_user_by_email'}), name='get_user_by_email'),
    path('users/test/', UserManagementHandler.as_view({'post': 'create_user'}), name='create_user'),
    path('users/id/', UserManagementHandler.as_view({'delete': 'delete_user'}), name='delete_user'),
]
