from django.urls import path
from . import views

urlpatterns = [
    path('path/<int:pk>/', views.path_detail, name='path_detail'),
]
