'''Defines URL schemes fro learning_logs'''

from django.urls import path

from . import views
from .views import InfoListView

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'), # Home page 
    path('topics/', views.topics, name='topics'), # Page with a list of all topics
    path('topics/<int:topic_id>/', views.topic, name='topic'), # Page with an addition information about topic
    path('new_topic/', views.new_topic, name='new_topic'), # Page for creating new topics
    path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'), # Page for creating new entries 
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'), # Page for editing entries
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('delete_entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('search_test/', InfoListView.as_view(), name='main-view'),
]