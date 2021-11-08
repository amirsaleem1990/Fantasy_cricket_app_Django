from django.conf.urls import url
from .views import *
from django.urls import include, path

urlpatterns = [
    url("create_team",         create_team,        name="create_team"       ),
    url("my_form",             my_form,            name="my_form"           ),
    url("ajax_creation_form/", ajax_creation_form, name="ajax_creation_form"),
]

