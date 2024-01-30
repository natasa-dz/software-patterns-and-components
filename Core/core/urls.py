from django.urls import path

from core import views

urlpatterns = [
    path('', views.base, name='base')
]