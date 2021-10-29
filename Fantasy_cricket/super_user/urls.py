from django.conf.urls import url
from .views import *
from django.urls import include

urlpatterns = [
    url("create_new_country_func", create_new_country_func, name="create_new_country_func"), # myapp.views.hello
]