from django.urls import path

from Core.core import views

urlpatterns = [
    path('', views.base, name='base')
]