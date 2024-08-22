import random
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse 
from .models import Path, Module, StudentProgress, Lesson, Question


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


def quiz_lesson_detail(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    module_id = request.GET.get('module_id')
    
    # Randomise order of answers for eac question
    questions = []
    for question in lesson.quiz_questions.all():
        answers = [question.correct_answer, question.incorrect_answer_1, question.incorrect_answer_2, question.incorrect_answer_3]
        answers = [a for a in answers if a]  # Remove any None values
        random.shuffle(answers)
        questions.append({
            'question': question,
            'answers': answers
        })

    if request.method == 'POST':
        correct_answers_count = 0
        total_questions = len(questions)

        # Iterate through the user's answers and calculate correct answers
        for q in questions:
            selected_answer = request.POST.get(f'question_{q["question"].pk}')
            if selected_answer == q['question'].correct_answer:
                correct_answers_count += 1

        score = (correct_answers_count / total_questions) * 100
        passed = score >= lesson.passing_percentage

        # Update student progress if passed
        if passed:
            progress, created = StudentProgress.objects.get_or_create(student=request.user, lesson=lesson)
            progress.completed = True
            progress.points = lesson.points
            progress.save()

        # Redirect to results page with score, passed status, and module_id as query parameters
        return HttpResponseRedirect(f"{reverse('quiz_results', args=[lesson.id])}?score={score}&passed={passed}&module_id={module_id}")

    module_url = reverse('module_detail', args=[module_id]) if module_id else reverse('module_detail', args=[lesson.modules.first().pk])

    context = {
        'lesson': lesson,
        'questions': questions,
        'module_url': module_url,
    }

    return render(request, 'content/quiz_lesson_detail.html', context)



def quiz_results(request, pk):
    lesson = get_object_or_404(Lesson, pk=pk)
    
    try:
        score = float(request.GET.get('score', 0))
        passed = request.GET.get('passed') == 'True'
    except (ValueError, TypeError):
        return HttpResponseBadRequest("Invalid request data.")
    
    module_id = request.GET.get('module_id')
    module_url = reverse('module_detail', args=[module_id]) if module_id else reverse('module_detail', args=[lesson.modules.first().pk])

    total_questions = lesson.quiz_questions.count()
    correct_answers_count = int((score / 100) * total_questions)

    context = {
        'lesson': lesson,
        'total_questions': total_questions,
        'correct_answers': correct_answers_count,
        'score': score,
        'passed': passed,
        'module_url': module_url,
    }

    return render(request, 'content/quiz_results.html', context)


