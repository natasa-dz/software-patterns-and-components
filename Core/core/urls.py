from django.urls import path

from core import views

urlpatterns = [
    path('', views.base, name='base'),
    path('simple_visualization_data_processing/', views.simple_visualization_data_processing, name='simple_visualization_data_processing'),
    path('apply_query/', views.apply_query, name='queries'),

]