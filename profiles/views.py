from django.shortcuts import render
from .models import Profile, Module, StudentProgress
from .badges import BADGES

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

    # Get all paths assigned to user
    assigned_paths = user_profile.assigned_paths.all()
    total_paths_count = assigned_paths.count()

    # Calculate completed paths using the method in Profile
    completed_paths = user_profile.get_completed_paths()
    completed_paths_count = len(completed_paths)

    # Use sets to ensure only unique lessons/modules are counted
    completed_modules = set()
    completed_lessons = set()
    total_modules = set()
    total_lessons = set()

    # Calculate completed and total modules and lessons
    for path in assigned_paths:
        for module in path.modules.all():
            total_modules.add(module.id)
            # Check if the module is fully completed
            if user_profile.is_module_completed(module):
                completed_modules.add(module.id)

            # Track lessons distinctly
            lessons = module.lessons.all()
            for lesson in lessons:
                total_lessons.add(lesson.id)
                if StudentProgress.objects.filter(student=request.user, lesson=lesson, completed=True).exists():
                    completed_lessons.add(lesson.id)

    # Count distinct completed modules/lessons
    completed_modules_count = len(completed_modules)
    completed_lessons_count = len(completed_lessons)
    total_modules_count = len(total_modules)
    total_lessons_count = len(total_lessons)

    # Calculate incomplete counts
    incomplete_paths_count = total_paths_count - completed_paths_count
    incomplete_modules_count = total_modules_count - completed_modules_count
    incomplete_lessons_count = total_lessons_count - completed_lessons_count

    # Calculate the percentage of lessons completed
    if total_lessons_count > 0:
        lesson_completion_percentage = (completed_lessons_count / total_lessons_count) * 100
    else:
        lesson_completion_percentage = 0

    # Leaderboard data with anonymised names, excluding students who have not yet acquired points
    cohort_profiles = Profile.objects.filter(cohort=user_profile.cohort, points__gt=0).order_by('-points')
    leaderboard_labels = [
        profile.user.username if profile.user == request.user else "Student"
        for profile in cohort_profiles
    ]
    leaderboard_data = [profile.points for profile in cohort_profiles]

    context = {
        'completed_paths_count': completed_paths_count,
        'incomplete_paths_count': incomplete_paths_count,
        'completed_modules_count': completed_modules_count,
        'incomplete_modules_count': incomplete_modules_count,
        'completed_lessons_count': completed_lessons_count,
        'incomplete_lessons_count': incomplete_lessons_count,
        'user_role': user_profile.role,
        'leaderboard_labels': leaderboard_labels,
        'leaderboard_data': leaderboard_data,
        'lesson_completion_percentage': lesson_completion_percentage,
        'daily_streak': user_profile.daily_streak,
    }

    return render(request, 'profiles/dashboard.html', context)

def badges_view(request):
    profile = request.user.profile
    
    badges = [
        {
            'name': badge['name'],
            'description': badge['description'],
            'icon': badge['icon'],
            'achieved': badge['condition'](profile),
        }
        for badge in BADGES
    ]

    context = {
        'badges': badges,
        'user_role': profile.role,
    }
    
    return render(request, 'profiles/badges.html', context)