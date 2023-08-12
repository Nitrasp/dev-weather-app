# weather/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('daily/', views.InitView.as_view(), name='daily'),
    path('daily/<str:country>/', views.InitView.as_view(), name='daily'),
    path('weekly/', views.InitView.as_view(), name='weekly'),
    path('weekly/<str:country>/', views.InitView.as_view(), name='weekly'),
]
