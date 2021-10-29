from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("", super_user, name="super_user"), # myapp.views.hello
]