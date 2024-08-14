from django.shortcuts import render
from .models import Profile

def profile(request):
    user_profile = request.user.profile

    # Get assigned paths for all roles
    assigned_paths = user_profile.assigned_paths.all()

    # Get completed paths for all roles
    completed_paths = user_profile.get_completed_paths()

    context = {
        'assigned_paths': assigned_paths,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }

    return render(request, 'profiles/profile.html', context)
