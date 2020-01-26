"""MyRegist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from login import views

urlpatterns = [
    path('admin/', admin.site.urls),        # 后台管理界面
    path('index/', views.index),            # 主页
    path('login/', views.login),            # 登录界面
    path('register/', views.register),      # 注册界面
    path('logout/', views.logout),          # 登出界面
    path('captcha', include('captcha.urls')),   # 图片验证码
    path('confirm/', views.user_confirm),   # 邮箱验证码
]
