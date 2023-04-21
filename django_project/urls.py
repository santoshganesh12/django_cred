"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', views.account_list, name='account_list'),
    path('accounts/<int:account_id>/', views.account_detail, name='account_detail'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:destination_id>/', views.destination_detail, name='destination_detail'),
    path('destinations/<int:account_id>/', views.destination_list_for_account, name='destination_list_for_account'),
    path('server/incoming_data/', views.incoming_data, name='incoming_data'),
    path('webhook/', views.webhook_receiver, name='webhook_receiver'),
]
