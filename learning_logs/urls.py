'''Defines URL schemes fro learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'), # Home page 
    path('topics/', views.topics, name='topics'), # Page with a list of all topics
    path('topics/<int:topic_id>/', views.topic, name='topic'), # Page with an addition information about topic
    path('new_topic/', views.new_topic, name='new_topic'), # Page for creating new topics
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'), # Page for creating new entries 
]