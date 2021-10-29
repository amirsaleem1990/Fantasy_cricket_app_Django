from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("", auth, name="auth"), # myapp.views.hello
]