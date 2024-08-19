from django.db import models
from django.contrib.auth.models import User
from content.models import Path, Module, StudentProgress
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('trainer', 'Trainer'),
        ('manager', 'Manager'),
    ]
    COHORT_CHOICES = [
        ('Cohort 1', 'Cohort 1'),
        ('Cohort 2', 'Cohort 2'),
        ('Cohort 3', 'Cohort 3'),
        ('Cohort 4', 'Cohort 4'),
        ('Cohort 5', 'Cohort 5'),
        ('Cohort 6', 'Cohort 6'),
        ('Cohort 7', 'Cohort 7'),
        ('Cohort 8', 'Cohort 8'),
        ('Cohort 9', 'Cohort 9'),
        ('Cohort 10', 'Cohort 10'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    cohort = models.CharField(max_length=20, choices=COHORT_CHOICES, blank=True, null=True)
    assigned_paths = models.ManyToManyField(Path, related_name='students', blank=True)
    points = models.PositiveIntegerField(default=0)
    daily_streak = models.PositiveIntegerField(default=0)
    last_completion_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_assigned_modules(self):
        # Get all modules related to the paths assigned to the student
        assigned_modules = Module.objects.filter(paths__in=self.assigned_paths.all()).distinct()
        return assigned_modules

    def get_completed_paths(self):
        # Check for completed paths
        completed_paths = []
        for path in self.assigned_paths.all():
            all_modules_completed = True
            for module in path.modules.all():
                if not self.is_module_completed(module):
                    all_modules_completed = False
                    break
            if all_modules_completed:
                completed_paths.append(path)
        return completed_paths

    def is_module_completed(self, module):
        # Check if all lessons in the module are completed by the student
        lessons = module.lessons.all()
        completed_lessons = StudentProgress.objects.filter(student=self.user, lesson__in=lessons, completed=True).count()
        return completed_lessons == lessons.count()

    def update_daily_streak(self):
        today = timezone.now().date()
        if self.last_completion_date == today - timedelta(days=1):
            self.daily_streak += 1
        elif self.last_completion_date != today:
            self.daily_streak = 1
        self.last_completion_date = today
        self.save(update_fields=['daily_streak', 'last_completion_date'])
