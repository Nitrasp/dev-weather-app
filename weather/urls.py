# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('week/', views.InitView.as_view(), name='weather'),
]
