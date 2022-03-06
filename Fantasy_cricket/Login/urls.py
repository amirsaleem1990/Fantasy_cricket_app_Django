from django.conf.urls import url
from . import views as login_views
from django.urls import include


urlpatterns = [
    url("", login_views.auth, name="auth"),
]