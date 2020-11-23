"""myweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views



urlpatterns = [
    path('search/', views.ytindex, name='ytindex'),
    path('', views.index),
    path('home/', views.home),
    path('search_title/', views.search_title),
    path('login_action/', views.login_action),  #新增login_action配置
    path('logout/',views.logout),  #新增登出路徑
    
]
