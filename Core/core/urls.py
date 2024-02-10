from django.urls import path

from Core.core import views

urlpatterns = [
    path('', views.base, name='base'),
    path('simple_visualization_data_processing/', views.simple_visualization_data_processing,
         name='simple_visualization_data_processing'),
    path('complex_visualization_data_processing/', views.complex_visualization_data_processing,
         name='complex_visualization_data_processing'),
]
