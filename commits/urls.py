from django.urls import path
from .api import get_commits

urlpatterns = [
    path('commits/', get_commits, name='get_commits'),
]