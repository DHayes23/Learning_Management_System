from django.shortcuts import render
from .models import Profile, Module

def profile(request):
    user_profile = request.user.profile

    # Get assigned paths for all roles
    assigned_paths = user_profile.assigned_paths.all()

    # Get completed paths for all roles
    completed_paths = user_profile.get_completed_paths()

    # Add a flag to each path indicating if it's completed
    paths_with_completion_status = []
    for path in assigned_paths:
        path.is_completed = path in completed_paths
        path.modules_with_completion_status = []
        for module in path.modules.all():
            module.is_completed = module.is_completed_by_student(request.user)
            path.modules_with_completion_status.append(module)
        paths_with_completion_status.append(path)

    context = {
        'assigned_paths': paths_with_completion_status,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }

    return render(request, 'profiles/profile.html', context)
