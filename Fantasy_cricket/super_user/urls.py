from django.conf.urls import url
from . import views as super_user_views
from django.urls import include, path

urlpatterns = [
    url("create_new_country", super_user_views.create_new_country_func, name="create_new_country" ),
    url("create_new_match", super_user_views.create_new_match_func, name="create_new_match" ),
    path('ajax/load-cities/', super_user_views.load_cities, name='ajax_load_cities' ), # AJAX
    url("match_created", super_user_views.match_created, name="match_created" ),
    url("record_performance", super_user_views.record_performance_func, name="record_performance" ),
    path('/record/<slug:teams>/<int:id_>/', super_user_views.leader_board_and_record_performance, name="leader_board_and_record_performance"),
    url("record_a_score", super_user_views.record_a_score_func, name="record_a_score"),
    url("Create_new_country", super_user_views.Create_new_country, name="Create_new_country" ),
    url("ajax_score_form/", super_user_views.ajax_score_form, name="ajax_score_form"    ),
]