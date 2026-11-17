from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('404/', views.error_404, name='error_404'),
]