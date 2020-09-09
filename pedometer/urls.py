"""pedometer URL Configuration

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
from pedometerapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout_request, name='logout'),
    path('login/', views.login_request, name='login'),
    path('stats/', views.stats, name='stats'),
    path('create_activity/', views.create_activity, name='create_activity'),
    path('search/', views.search, name='search'),
    path('test/', views.test, name='test'),
    path('process_search/', views.processSearch, name='process'),
    path('process_search2/', views.processSearch2, name='process2'),
    
    path('', views.index, name='index'),
    #path('pedometerapp/',include('pedometerapp.urls')),
]
