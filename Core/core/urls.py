from django.urls import path

from Core.core import views

urlpatterns = [
    path('', views.base, name='base'),
    path('simple-visualization/', views.simple_visualization, name='simple_visualization'),
    path('complex-visualization/', views.complex_visualization, name='complex_visualization'),
]
