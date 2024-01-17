from django.urls import path
from .api import post_commits

urlpatterns = [
    path('commits/', post_commits, name='get_commits'),
]