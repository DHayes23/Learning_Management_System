from django.urls import path
from . import views

urlpatterns = [
    path('path/<int:pk>/', views.path_detail, name='path_detail'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
]
