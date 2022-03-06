from django.conf.urls import url
from . import views as normal_user_views

from django.urls import include, path

urlpatterns = [
    url("create_team", normal_user_views.create_team, name="create_team"),
    url("my_form", normal_user_views.my_form, name="my_form"),
    url("ajax_creation_form/", normal_user_views.ajax_creation_form, name="ajax_creation_form"),
    url("team_performance", normal_user_views.team_performance, name="team_performance.html"),
    url("leader_board", normal_user_views.leader_board, name="leader_board"),
]

