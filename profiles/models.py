from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.user.username
