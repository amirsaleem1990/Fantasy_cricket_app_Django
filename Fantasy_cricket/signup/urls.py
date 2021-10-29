from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("", create_user, name="create_user"),
]