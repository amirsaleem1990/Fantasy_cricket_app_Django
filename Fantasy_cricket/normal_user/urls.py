from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("create_team", create_team, name="create_team"),
]