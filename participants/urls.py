from django.urls import path

from . import views

urlpatterns = [
    path('', views.participant_list, name='participant_list'),
    path('<int:tournament_id>/', views.participant_list, name='participant_list_by_tournament'),
]