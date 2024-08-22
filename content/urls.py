from django.urls import path
from . import views
from .views import text_lesson_detail, video_lesson_detail, quiz_lesson_detail, deliverable_lesson_detail


urlpatterns = [
    path('path/<int:pk>/', views.path_detail, name='path_detail'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),
    path('lesson/text/<int:pk>/', text_lesson_detail, name='text_lesson_detail'),
    path('lesson/video/<int:pk>/', video_lesson_detail, name='video_lesson_detail'),
    path('lesson/quiz/<int:pk>/', quiz_lesson_detail, name='quiz_lesson_detail'),
    path('lesson/deliverable/<int:pk>/', deliverable_lesson_detail, name='deliverable_lesson_detail'),
    path('lesson/quiz/<int:pk>/results/', views.quiz_results, name='quiz_results'),
    path('module/<int:pk>/', views.module_detail, name='module_detail'),

]
