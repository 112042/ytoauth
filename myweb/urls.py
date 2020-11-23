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
from django.conf.urls import url,include
from django.urls import path
from django.contrib import admin
from rest_framework import routers
from webview import views



router = routers.DefaultRouter()
#router.register(r'users', views.UserViewSet)
#router.register(r'groups', views.GroupViewSet)
router.register(r'books', views.booksViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)



urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^restful',include(router.urls)),
	url(r'^api-auth/',include('rest_framework.urls',namespace='rest_framework')),
    path('', include('webview.urls')),
    #path('', include('accounts.urls')),  # 自己的應用程式網址
    path('accounts/', include('allauth.urls')),  # django-allauth網址
     
    
    
]