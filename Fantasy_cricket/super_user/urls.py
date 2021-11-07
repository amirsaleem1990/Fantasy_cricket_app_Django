from django.conf.urls import url
from .views import *
from django.urls import include, path
urlpatterns = [
    url("create_new_country",      create_new_country_func,             name="create_new_country" ),
    url("create_new_match",        create_new_match_func,               name="create_new_match"   ),
    path('ajax/load-cities/',      load_cities,                         name='ajax_load_cities'   ), # AJAX
    url("match_created",           match_created,                       name="match_created"      ),
    url("record_performance",      record_performance_func ,            name="record_performance" ),
    path('/record/<slug:teams>/<int:id_>/',  leader_board_and_record_performance, name="leader_board_and_record_performance"),
    url("record_a_score",          record_a_score_func,                 name="record_a_score"),
]