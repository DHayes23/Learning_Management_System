from django.shortcuts import render
from .models import Profile, Module, StudentProgress

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
            module.total_lessons = module.lessons.count()
            # Calculate completed lessons for the current module
            module.completed_lessons = StudentProgress.objects.filter(
                student=request.user,
                lesson__in=module.lessons.all(),
                completed=True
            ).count()
            path.modules_with_completion_status.append(module)
        paths_with_completion_status.append(path)

    context = {
        'assigned_paths': paths_with_completion_status,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }

    return render(request, 'profiles/profile.html', context)

def dashboard(request):
    user_profile = request.user.profile

    assigned_paths = user_profile.assigned_paths.all()
    completed_paths = user_profile.get_completed_paths()
    
    context = {
        'assigned_paths': assigned_paths,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }

    return render(request, 'profiles/dashboard.html', context)
