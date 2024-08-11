from django.urls import path
from . import views
from .decorators import role_required

urlpatterns = [
    path('profile/', role_required(['student', 'trainer', 'manager'])(views.profile), name='profile'),
]
