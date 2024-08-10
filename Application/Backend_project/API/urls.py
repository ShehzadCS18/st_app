from django.urls import path
from .views import greet_view, segment_view

urlpatterns = [
    path('greet/', greet_view, name='greet'),
    path('segment/', segment_view, name='segment'),
]
