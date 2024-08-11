from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import Path, Module, Lesson, StudentProgress
from profiles.models import Profile
from profiles.decorators import role_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

class ProfileModelTest(TestCase):
    
    def test_profile_creation(self):
        # Test that a profile is automatically created when a new user is created
        user = User.objects.create(username='testuser', password='testpassword')
        self.assertTrue(Profile.objects.filter(user=user).exists(), "Profile should be created when a new user is created.")

    def test_default_role_assignment(self):
        # Test that the default role assigned to a new profile is 'Student'
        user = User.objects.create(username='testuser', password='testpassword')
        self.assertEqual(user.profile.role, 'student', "The default role should be 'Student'.")

    def test_cohort_choices(self):
        # Test that the cohort choices are correctly defined in the Profile model
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

class StudentProgressTest(TestCase):

    def setUp(self):
        # Create users, paths, modules, and lessons for testing
        self.user = User.objects.create(username='student', password='testpassword123')
        self.profile = self.user.profile
        self.path1 = Path.objects.create(name='Path 1')
        self.path2 = Path.objects.create(name='Path 2')
        self.module1 = Module.objects.create(name='Module 1')
        self.module2 = Module.objects.create(name='Module 2')
        self.lesson1 = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.lesson2 = Lesson.objects.create(name='Lesson 2', lesson_type='video')
        self.lesson3 = Lesson.objects.create(name='Lesson 3', lesson_type='quiz')

    def test_assigning_path_creates_student_progress(self):
        # Test that assigning a path to a student creates the correct StudentProgress entries
        self.module1.lessons.add(self.lesson1, self.lesson2)
        self.path1.modules.add(self.module1)
        self.profile.assigned_paths.add(self.path1)

        self.assertEqual(StudentProgress.objects.filter(student=self.user).count(), 2, "StudentProgress should be created for each lesson in the assigned path.")

    def test_removing_path_deletes_student_progress(self):
        # Test that removing a path deletes the correct StudentProgress entries
        self.module1.lessons.add(self.lesson1, self.lesson2)
        self.path1.modules.add(self.module1)
        self.profile.assigned_paths.add(self.path1)

        # Now remove the path
        self.profile.assigned_paths.remove(self.path1)

        self.assertEqual(StudentProgress.objects.filter(student=self.user).count(), 0, "StudentProgress should be deleted when a path is removed.")

    def test_overlapping_modules_handle_progress_correctly(self):
        # Test that overlapping modules/lessons are handled correctly in StudentProgress
        self.module1.lessons.add(self.lesson1, self.lesson2)
        self.module2.lessons.add(self.lesson2, self.lesson3)
        self.path1.modules.add(self.module1)
        self.path2.modules.add(self.module2)

        self.profile.assigned_paths.add(self.path1)
        self.profile.assigned_paths.add(self.path2)

        # Remove path1, which shares lesson2 with path2
        self.profile.assigned_paths.remove(self.path1)

        # lesson2 should not be deleted because it's still in path2
        self.assertTrue(StudentProgress.objects.filter(student=self.user, lesson=self.lesson2).exists(), "StudentProgress for lesson2 should not be deleted because it's still part of path2.")
        self.assertEqual(StudentProgress.objects.filter(student=self.user).count(), 2, "Only lesson1's progress should be deleted, leaving lesson2 and lesson3.")

    def test_removing_module_from_path_updates_student_progress(self):
        # Test that removing a module from a path updates StudentProgress entries correctly
        self.module1.lessons.add(self.lesson1, self.lesson2)
        self.module2.lessons.add(self.lesson3)
        self.path1.modules.add(self.module1, self.module2)
        self.profile.assigned_paths.add(self.path1)

        # Now remove the module1
        self.path1.modules.remove(self.module1)

        self.assertFalse(StudentProgress.objects.filter(student=self.user, lesson=self.lesson1).exists(), "StudentProgress for lesson1 should be deleted because its module was removed.")
        self.assertTrue(StudentProgress.objects.filter(student=self.user, lesson=self.lesson3).exists(), "StudentProgress for lesson3 should still exist because it's in another module.")

class RoleBasedAccessControlTest(TestCase):

    def setUp(self):
        # Set up different roles for testing role-based access control
        self.student_user = User.objects.create(username='student', password='testpassword123')
        self.trainer_user = User.objects.create(username='trainer', password='testpassword123')
        self.trainer_user.profile.role = 'trainer'
        self.trainer_user.profile.save()

    def mock_view(self, request):
        # Mock view for testing role-based access control
        return HttpResponse("Access granted")

    def test_access_for_student(self):
        # Test that students do not have access to views restricted to trainers/managers
        request = self.client.get('/mock-path/')
        request.user = self.student_user
        decorated_view = role_required(['trainer', 'manager'])(self.mock_view)
        with self.assertRaises(PermissionDenied):
            decorated_view(request)

    def test_access_for_trainer(self):
        # Test that trainers have access to views restricted to trainers/managers
        request = self.client.get('/mock-path/')
        request.user = self.trainer_user
        decorated_view = role_required(['trainer', 'manager'])(self.mock_view)
        response = decorated_view(request)
        self.assertEqual(response.status_code, 200, "Trainers should have access to this view.")
