'''Defines URL schemes fro learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'), # Home page 
]