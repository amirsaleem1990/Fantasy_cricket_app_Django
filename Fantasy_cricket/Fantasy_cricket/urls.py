"""Fantasy_cricket URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.views.generic import TemplateView
from django.conf.urls import include, url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="Login/login.html")),
    # path('Create_new_country', TemplateView.as_view(template_name="super_user/Create_new_country.html")),
    path('signup', TemplateView.as_view(template_name="signup/signup.html")),
    
    url("login", include("Login.urls")),
    url("signup_", include("signup.urls")),
    url("normal_user/", include("normal_user.urls")),
    url("super_user", include("super_user.urls")),
    url("create_new_match", include("super_user.urls")),
    url("Create_new_country", include("super_user.urls")),
    
]