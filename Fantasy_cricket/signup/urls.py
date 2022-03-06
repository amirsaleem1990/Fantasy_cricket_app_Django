from django.conf.urls import url
from . import views as signup_views
from django.urls import include

urlpatterns = [
    url("", signup_views.create_user, name="create_user"),
]