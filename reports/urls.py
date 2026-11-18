from django.urls import path

from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.report_index, name='report_index'),
    path('tournaments/', views.tournament_list_report,
         name='tournament_list_report'),
    path(
        'tournaments/<int:tournament_id>/participants/',
        views.tournament_participants_report,
        name='tournament_participants_report',
    ),
    path(
        'tournaments/<int:tournament_id>/matches/',
        views.tournament_matches_report,
        name='tournament_matches_report',
    ),
    path(
        'tournaments/<int:tournament_id>/results/',
        views.tournament_results_report,
        name='tournament_results_report',
    ),
    path(
        'tournaments/<int:tournament_id>/stats/',
        views.tournament_stats_report,
        name='tournament_stats_report',
    ),
    path('statistics/', views.overall_statistics_report,
         name='overall_statistics_report'),
]
