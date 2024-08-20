from django.shortcuts import render, get_object_or_404
from django.urls import reverse 
from .models import Path, Module, StudentProgress, Lesson

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

    # Add a flag to each lesson if it's completed by the user and generate the URL
    for lesson in lessons:
        lesson.is_completed = user_progress.filter(lesson=lesson, completed=True).exists()
        # Generate a URL for each lesson based on its type
        if lesson.lesson_type == 'text':
            lesson.url = reverse('text_lesson_detail', args=[lesson.pk])
        elif lesson.lesson_type == 'video':
            lesson.url = reverse('video_lesson_detail', args=[lesson.pk])
        elif lesson.lesson_type == 'quiz':
            lesson.url = reverse('quiz_lesson_detail', args=[lesson.pk])
        elif lesson.lesson_type == 'deliverable':
            lesson.url = reverse('deliverable_lesson_detail', args=[lesson.pk])

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

def text_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    module_url = reverse('module_detail', args=[lesson.modules.first().pk])

    user_profile = request.user.profile

    context = {
        'lesson': lesson,
        'module_url': module_url,
        'user_role': user_profile.role,
    }

    return render(request, 'content/text_lesson_detail.html', context)

def video_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    # Handle the case where the video URL is missing
    if lesson.video_url and 'youtube.com/watch' in lesson.video_url:
        video_id = lesson.video_url.split('v=')[1]
        embed_url = f'https://www.youtube.com/embed/{video_id}'
    else:
        embed_url = None

    module_url = reverse('module_detail', args=[lesson.modules.first().pk])

    user_profile = request.user.profile

    context = {
        'lesson': lesson,
        'embed_url': embed_url,
        'module_url': module_url,
        'user_role': user_profile.role,
    }

    return render(request, 'content/video_lesson_detail.html', context)

def quiz_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    module_url = reverse('module_detail', args=[lesson.modules.first().pk])

    user_profile = request.user.profile

    context = {
        'lesson': lesson,
        'module_url': module_url,
        'user_role': user_profile.role,
    }

    return render(request, 'content/quiz_lesson_detail.html', context)

def deliverable_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)

    module_url = reverse('module_detail', args=[lesson.modules.first().pk])

    user_profile = request.user.profile

    context = {
        'lesson': lesson,
        'module_url': module_url,
        'user_role': user_profile.role,
    }

    return render(request, 'content/deliverable_lesson_detail.html', context)
