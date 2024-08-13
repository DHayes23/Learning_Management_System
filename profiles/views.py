from django.shortcuts import render
from .models import Profile

def profile(request):
    user_profile = request.user.profile

    if user_profile.role == 'student':
        # Get assigned paths for the student
        assigned_paths = user_profile.assigned_paths.all()
        completed_paths = user_profile.get_completed_paths()
        context = {
            'assigned_paths': assigned_paths,
            'completed_paths': completed_paths,
        }
    elif user_profile.role == 'trainer':
        context = {}
    elif user_profile.role == 'manager':
        context = {}

    return render(request, 'profiles/profile.html', context)
