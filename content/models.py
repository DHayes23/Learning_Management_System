from django.db import models
from django.contrib.auth.models import User

class Path(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    modules = models.ManyToManyField('Module', related_name='paths', blank=True)

    def is_completed_by_student(self, student):
        modules = self.modules.all()
        completed_modules = sum(1 for module in modules if module.is_completed_by_student(student))
        return completed_modules == modules.count()

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lessons = models.ManyToManyField('Lesson', related_name='modules', blank=True)

    def is_completed_by_student(self, student):
        lessons = self.lessons.all()
        completed_lessons = StudentProgress.objects.filter(student=student, lesson__in=lessons, completed=True).count()
        return completed_lessons == lessons.count()

    def __str__(self):
        return self.name

class Lesson(models.Model):
    LESSON_TYPES = [
        ('text', 'Text Based'),
        ('video', 'Video Based'),
        ('quiz', 'Quiz/Assessment'),
        ('deliverable', 'Deliverable'),
    ]
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES)
    content = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.get_lesson_type_display()})"

class StudentProgress(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'lesson')

    def __str__(self):
        return f"{self.student.username} - {self.lesson.name} ({'Completed' if self.completed else 'Incomplete'})"
