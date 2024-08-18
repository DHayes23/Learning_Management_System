from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    modules = models.ManyToManyField('Module', related_name='paths', blank=True)

    def is_completed_by_student(self, student):
        modules = self.modules.all()
        completed_modules = sum(1 for module in modules if module.is_completed_by_student(student))
        return completed_modules == modules.count()

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    lessons = models.ManyToManyField('Lesson', related_name='modules', blank=True)

    def is_completed_by_student(self, student):
        lessons = self.lessons.all()
        completed_lessons = StudentProgress.objects.filter(student=student, lesson__in=lessons, completed=True).count()
        return completed_lessons == lessons.count()

    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.TextField()
    correct_answer = models.CharField(max_length=255)
    incorrect_answer_1 = models.CharField(max_length=255)
    incorrect_answer_2 = models.CharField(max_length=255, blank=True, null=True)
    incorrect_answer_3 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.question_text

class Lesson(models.Model):
    LESSON_TYPES = [
        ('text', 'Text Based'),
        ('video', 'Video Based'),
        ('quiz', 'Quiz/Assessment'),
        ('deliverable', 'Deliverable'),
    ]

    DIFFICULTY_LEVELS = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    # Generic lesson fields
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    points = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='medium')
    time_to_complete = models.PositiveIntegerField(default=10, verbose_name="Time to Complete (Minutes)") # Default 10 minutes

    # Fields specific to certain lesson types
    video_url = models.URLField(blank=True, null=True)
    quiz_questions = models.ManyToManyField('Question', blank=True, related_name='lessons')
    passing_percentage = models.PositiveIntegerField(blank=True, null=True, default=70)  # Default 70%
    due_date = models.DateField(blank=True, null=True)
    recipient_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_lesson_type_display() if self.lesson_type else 'No Type'})"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    points = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.name} ({'Completed' if self.completed else 'Incomplete'})"
