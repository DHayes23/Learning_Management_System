from django.shortcuts import render, get_object_or_404
from .models import Path, Module, StudentProgress

def path_detail(request, pk):
    path = get_object_or_404(Path, pk=pk)

    # Get assigned paths and completed paths for the current user
    user_profile = request.user.profile
    assigned_paths = user_profile.assigned_paths.all()
    completed_paths = user_profile.get_completed_paths()

    context = {
        'path': path,
        'assigned_paths': assigned_paths,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }
    
    return render(request, 'content/path_detail.html', context)

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = module.lessons.all()
    user_progress = StudentProgress.objects.filter(student=request.user)
    
    # Add a flag to each lesson if it's completed by the user
    for lesson in lessons:
        lesson.is_completed = user_progress.filter(lesson=lesson, completed=True).exists()

    # Get assigned paths and completed paths for the current user
    user_profile = request.user.profile
    assigned_paths = user_profile.assigned_paths.all()
    completed_paths = user_profile.get_completed_paths()

    context = {
        'module': module,
        'lessons': lessons,
        'assigned_paths': assigned_paths,
        'completed_paths': completed_paths,
        'user_role': user_profile.role,
    }

    return render(request, 'content/module_detail.html', context)
