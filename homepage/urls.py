from django.urls import path

from . import views

app_name = 'homepage'

urlpatterns = [
    path('', views.home, name='home'),
    path('404/', views.error_404, name='error_404'),
]
