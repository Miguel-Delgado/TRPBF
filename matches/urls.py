from django.urls import path

from . import views

urlpatterns = [
    path('', views.match_list, name='match_list'),
    path('<int:tournament_id>/', views.match_list, name='match_list_by_tournament'),
]