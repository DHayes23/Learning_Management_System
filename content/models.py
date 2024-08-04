from django.db import models

class Path(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    modules = models.ManyToManyField('Module', related_name='paths', blank=True)

    def __str__(self):
        return self.name

class Module(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

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
    module = models.ForeignKey(Module, related_name='lessons', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_lesson_type_display()})"
