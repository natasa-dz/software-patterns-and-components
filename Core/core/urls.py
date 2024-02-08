from django.urls import path

from core import views

urlpatterns = [
    path('', views.base, name='base'),
    path('simple-visualization/', views.simple_visualization, name='simple_visualization'),

]