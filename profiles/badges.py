from datetime import timedelta
from django.utils import timezone
from content.models import StudentProgress
from profiles.models import Profile

def has_1000_points(profile):
    return profile.points >= 1000

def has_7_day_streak(profile):
    return profile.daily_streak >= 7

def has_14_day_streak(profile):
    return profile.daily_streak >= 14

def has_completed_3_paths(profile):
    return len(profile.get_completed_paths()) >= 3

def has_completed_10_paths(profile):
    return len(profile.get_completed_paths()) >= 10

def has_completed_10_lessons_in_week(profile):
    one_week_ago = timezone.now() - timedelta(days=7)
    recent_lessons = StudentProgress.objects.filter(
        student=profile.user,
        completed=True,
        date_completed__gte=one_week_ago
    ).count()
    return recent_lessons >= 10

def has_completed_first_lesson(profile):
    return StudentProgress.objects.filter(student=profile.user, completed=True).exists()

def has_completed_5_lessons(profile):
    completed_lessons = StudentProgress.objects.filter(student=profile.user, completed=True).count()
    return completed_lessons >= 5


BADGES = [
    {
        'name': 'First Lesson Complete',
        'description': 'Completed your first lesson',
        'icon': 'fa-sharp fa-solid fa-check',
        'condition': has_completed_first_lesson
    },
    {
        'name': 'Five Lessons Complete',
        'description': 'Completed 5 lessons in total',
        'icon': 'fa-sharp fa-regular fa-tally',
        'condition': has_completed_5_lessons
    },
    {
        'name': '1000 Points',
        'description': 'Earned 1000 points',
        'icon': 'fa-sharp fa-solid fa-coins',
        'condition': has_1000_points
    },
    {
        'name': 'Lesson Sprinter',
        'description': 'Completed 10 lessons in a week',
        'icon': 'fa-sharp fa-solid fa-person-running-fast',
        'condition': has_completed_10_lessons_in_week
    },
    {
        'name': '7 Day Streak',
        'description': '7 days of continuous learning',
        'icon': 'fa-sharp fa-solid fa-fire',
        'condition': has_7_day_streak
    },
    {
        'name': '14 Day Streak',
        'description': '14 days of continuous learning',
        'icon': 'fa-sharp fa-solid fa-fire-flame-curved',
        'condition': has_14_day_streak
    },
    {
        'name': 'Pathfinder',
        'description': 'Completed 3 learning paths',
        'icon': 'fa-sharp fa-solid fa-route',
        'condition': has_completed_3_paths
    },
    {
        'name': 'Path Master',
        'description': 'Completed 10 learning paths',
        'icon': 'fa-sharp fa-solid fa-trophy',
        'condition': has_completed_10_paths
    },

]
