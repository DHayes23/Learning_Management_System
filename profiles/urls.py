from django.urls import path
from . import views
from .decorators import role_required
from .views import badges_view

urlpatterns = [
    path('profile/', role_required(['student', 'trainer', 'manager'])(views.profile), name='profile'),
    path('dashboard/', role_required(['student', 'trainer', 'manager'])(views.dashboard), name='dashboard'),
    path('badges/', badges_view, name='badges'),
]
