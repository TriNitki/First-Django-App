from django.urls import path, include

app_name = 'users'
urlpatterns = [
    # Turns on authorization by default
    path('', include('django.contrib.auth.urls')),
]