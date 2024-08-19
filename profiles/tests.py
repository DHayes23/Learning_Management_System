from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from content.models import Path, Module, Lesson, StudentProgress
from profiles.models import Profile
from profiles.decorators import role_required
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.test import Client
from django.utils import timezone
from datetime import timedelta

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

        # Remove the path
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

        # Remove module1
        self.path1.modules.remove(self.module1)

        self.assertFalse(StudentProgress.objects.filter(student=self.user, lesson=self.lesson1).exists(), "StudentProgress for lesson1 should be deleted because its module was removed.")
        self.assertTrue(StudentProgress.objects.filter(student=self.user, lesson=self.lesson3).exists(), "StudentProgress for lesson3 should still exist because it's in another module.")

    def test_date_completed_field_updated_on_completion(self):
        # Test that the date_completed field is set correctly when progress is marked as completed
        progress = StudentProgress.objects.create(student=self.user, lesson=self.lesson1, completed=False)
        self.assertIsNone(progress.date_completed, "date_completed should be None when progress is not completed.")
        
        progress.completed = True
        progress.save()

        progress.refresh_from_db()
        self.assertIsNotNone(progress.date_completed, "date_completed should be set when progress is marked as completed.")
        self.assertAlmostEqual(progress.date_completed, timezone.now(), delta=timezone.timedelta(seconds=10), msg="date_completed should be close to the current time when set.")

    def test_date_completed_field_reset_on_incomplete(self):
        # Test that the date_completed field is reset when progress is marked as incomplete
        progress = StudentProgress.objects.create(student=self.user, lesson=self.lesson1, completed=True, date_completed=timezone.now())
        self.assertIsNotNone(progress.date_completed, "date_completed should be set when progress is marked as completed.")

        progress.completed = False
        progress.save()

        progress.refresh_from_db()
        self.assertIsNone(progress.date_completed, "date_completed should be reset to None when progress is marked as incomplete.")

    def test_daily_streak_incremented_on_completion(self):
        # Test that daily streak is incremented when a lesson is completed
        self.profile.last_completion_date = timezone.now().date() - timedelta(days=1)
        self.profile.daily_streak = 1
        self.profile.save()

        progress = StudentProgress.objects.create(student=self.user, lesson=self.lesson1, completed=True)
        progress.save()

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_streak, 2, "Daily streak should be incremented by 1.")
        self.assertEqual(self.profile.last_completion_date, timezone.now().date(), "Last completion date should be updated to today.")

    def test_daily_streak_reset_after_gap(self):
        # Test that daily streak is reset if a day is skipped
        self.profile.last_completion_date = timezone.now().date() - timedelta(days=2)
        self.profile.daily_streak = 3
        self.profile.save()

        progress = StudentProgress.objects.create(student=self.user, lesson=self.lesson1, completed=True)
        progress.save()

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_streak, 1, "Daily streak should be reset to 1 after a gap.")
        self.assertEqual(self.profile.last_completion_date, timezone.now().date(), "Last completion date should be updated to today.")

    def test_no_streak_increment_for_multiple_completions_in_a_day(self):
        # Test that daily streak does not increment more than once per day
        self.profile.last_completion_date = timezone.now().date()
        self.profile.daily_streak = 5
        self.profile.save()

        progress = StudentProgress.objects.create(student=self.user, lesson=self.lesson1, completed=True)
        progress.save()

        progress2 = StudentProgress.objects.create(student=self.user, lesson=self.lesson2, completed=True)
        progress2.save()

        self.profile.refresh_from_db()
        self.assertEqual(self.profile.daily_streak, 5, "Daily streak should not increment more than once per day.")
        self.assertEqual(self.profile.last_completion_date, timezone.now().date(), "Last completion date should be today.")

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

class ProfileViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='testpassword')
        self.profile = self.user.profile
        self.path = Path.objects.create(name='Path 1')
        self.module = Module.objects.create(name='Module 1')
        self.lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.module.lessons.add(self.lesson)
        self.path.modules.add(self.module)
        self.profile.assigned_paths.add(self.path)
        self.client.login(username='student', password='testpassword')

    def test_profile_view_renders_correctly(self):
        # Test the profile view renders with correct context data
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertIn('assigned_paths', response.context)
        self.assertIn('completed_paths', response.context)
        self.assertIn('user_role', response.context)
        self.assertEqual(response.context['user_role'], self.profile.role)

    def test_profile_view_with_no_assigned_paths(self):
        # Test profile view when the user has no assigned paths
        self.profile.assigned_paths.clear()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['assigned_paths']), 0)
        self.assertEqual(len(response.context['completed_paths']), 0)

    def test_profile_view_completion_status(self):
        # Test profile view correctly marks paths and modules as completed or not
        progress, created = StudentProgress.objects.get_or_create(student=self.user, lesson=self.lesson, defaults={'completed': True})
        if not created:
            progress.completed = True
            progress.save()

        response = self.client.get(reverse('profile'))
        path = response.context['assigned_paths'][0]
        self.assertTrue(path in self.profile.get_completed_paths())
        module = path.modules_with_completion_status[0]
        self.assertTrue(module.is_completed_by_student(self.user))
        self.assertEqual(module.completed_lessons, 1)
        self.assertEqual(module.total_lessons, 1)

class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='student', password='testpassword')
        self.profile = self.user.profile
        self.path = Path.objects.create(name='Path 1')
        self.module = Module.objects.create(name='Module 1')
        self.lesson1 = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.lesson2 = Lesson.objects.create(name='Lesson 2', lesson_type='video')
        self.module.lessons.add(self.lesson1, self.lesson2)
        self.path.modules.add(self.module)
        self.profile.assigned_paths.add(self.path)
        self.client.login(username='student', password='testpassword')

    def test_dashboard_view_renders_correctly(self):
        # Test the dashboard view renders with correct context data
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/dashboard.html')
        self.assertIn('completed_paths_count', response.context)
        self.assertIn('incomplete_paths_count', response.context)
        self.assertIn('completed_modules_count', response.context)
        self.assertIn('incomplete_modules_count', response.context)
        self.assertIn('completed_lessons_count', response.context)
        self.assertIn('incomplete_lessons_count', response.context)
        self.assertIn('lesson_completion_percentage', response.context)
        self.assertIn('leaderboard_labels', response.context)
        self.assertIn('leaderboard_data', response.context)

    def test_dashboard_view_with_no_assigned_paths(self):
        # Test dashboard view when the user has no assigned paths
        self.profile.assigned_paths.clear()
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.context['completed_paths_count'], 0)
        self.assertEqual(response.context['incomplete_paths_count'], 0)
        self.assertEqual(response.context['completed_modules_count'], 0)
        self.assertEqual(response.context['completed_lessons_count'], 0)
        self.assertEqual(response.context['lesson_completion_percentage'], 0)

    def test_dashboard_view_leaderboard(self):
        # Test the leaderboard data in the dashboard view
        self.profile.points = 100
        self.profile.save()
        response = self.client.get(reverse('dashboard'))
        self.assertIn('leaderboard_labels', response.context)
        self.assertIn('leaderboard_data', response.context)
        self.assertEqual(response.context['leaderboard_labels'][0], 'student')
        self.assertEqual(response.context['leaderboard_data'][0], 100)
