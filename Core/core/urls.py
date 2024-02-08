from django.urls import path

from core import views

urlpatterns = [
    path('', views.base, name='base'),
    path('parse/', views.parse, name='parse'),
    path('index/', views.index, name='index')
]