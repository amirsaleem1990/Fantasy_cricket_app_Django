from django.conf.urls import url
from . import views as logout_views
from django.urls import include


urlpatterns = [
    url("", logout_views.logout, name="logout"),
]
