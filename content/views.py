from django.shortcuts import render, get_object_or_404
from .models import Path, Module, StudentProgress

def path_detail(request, pk):
    path = get_object_or_404(Path, pk=pk)
    return render(request, 'content/path_detail.html', {'path': path})

def module_detail(request, pk):
    module = get_object_or_404(Module, pk=pk)
    lessons = module.lessons.all()
    user_progress = StudentProgress.objects.filter(student=request.user)
    
    # Add a flag to each lesson if it's completed by the user
    for lesson in lessons:
        lesson.is_completed = user_progress.filter(lesson=lesson, completed=True).exists()

    return render(request, 'content/module_detail.html', {'module': module, 'lessons': lessons})
