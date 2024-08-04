from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from .decorators import role_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

class ProfileModelTest(TestCase):
    
    def test_profile_creation(self):
        user = User.objects.create(username='testuser', password='testpassword')
        self.assertTrue(Profile.objects.filter(user=user).exists(), "Profile should be created when a new user is created.")

    def test_default_role_assignment(self):
        user = User.objects.create(username='testuser', password='testpassword')
        self.assertEqual(user.profile.role, 'student', "The default role should be 'Student'.")

    def test_cohort_choices(self):
        cohort_choices = Profile.COHORT_CHOICES
        expected_choices = [
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
        self.assertEqual(cohort_choices, expected_choices, "Cohort choices should be present as defined.")


class RoleBasedAccessControlTest(TestCase):

    def setUp(self):
        self.student_user = User.objects.create(username='student', password='testpassword123')
        self.trainer_user = User.objects.create(username='trainer', password='testpassword123')
        self.trainer_user.profile.role = 'trainer'
        self.trainer_user.profile.save()

    def mock_view(self, request):
        return HttpResponse("Access granted")

    def test_access_for_student(self):
        request = self.client.get('/mock-path/')
        request.user = self.student_user
        decorated_view = role_required(['trainer', 'manager'])(self.mock_view)
        with self.assertRaises(PermissionDenied):
            decorated_view(request)

    def test_access_for_trainer(self):
        request = self.client.get('/mock-path/')
        request.user = self.trainer_user
        decorated_view = role_required(['trainer', 'manager'])(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200, "Trainers should have access to this view.")
