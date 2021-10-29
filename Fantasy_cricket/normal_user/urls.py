from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("", normal_user, name="normal_user"), # myapp.views.hello
]