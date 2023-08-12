# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.InitView.as_view(), name='daily'),
    path('daily/<str:city>/', views.InitView.as_view(), name='daily'),
    path('weekly/', views.InitView.as_view(), name='weekly'),
    path('weekly/<str:city>/', views.WeeklyView.as_view(), name='weekly'),
]
