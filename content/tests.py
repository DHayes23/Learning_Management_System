from django.test import TestCase
from .models import Path, Module, Lesson

class ContentModelTest(TestCase):
    
    def test_path_creation(self):
        # Test that a Path object can be created with the correct name and exists in the database
        path = Path.objects.create(name='Path 1', description='Test Path')
        self.assertEqual(path.name, 'Path 1', "Path should be created with the correct name.")
        self.assertEqual(Path.objects.count(), 1, "There should be one Path in the database.")

    def test_module_creation(self):
        # Test that a Module object can be created with the correct name and exists in the database
        module = Module.objects.create(name='Module 1', description='Test Module')
        self.assertEqual(module.name, 'Module 1', "Module should be created with the correct name.")
        self.assertEqual(Module.objects.count(), 1, "There should be one Module in the database.")

    def test_lesson_creation(self):
        # Test that a Lesson object can be created and associated with a Module
        module = Module.objects.create(name='Module 1')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        module.lessons.add(lesson)
        self.assertEqual(lesson.name, 'Lesson 1', "Lesson should be created with the correct name.")
        self.assertEqual(Lesson.objects.count(), 1, "There should be one Lesson in the database.")
        self.assertIn(lesson, module.lessons.all(), "Lesson should be correctly linked to its Module.")

    def test_path_module_relationship(self):
        # Test that Modules can be associated with a Path and retrieved correctly
        path = Path.objects.create(name='Path 1')
        module1 = Module.objects.create(name='Module 1')
        module2 = Module.objects.create(name='Module 2')
        path.modules.add(module1, module2)

        self.assertEqual(path.modules.count(), 2, "Path should have two modules.")
        self.assertIn(module1, path.modules.all(), "Path should contain 'Module 1'.")
        self.assertIn(module2, path.modules.all(), "Path should contain 'Module 2'.")

    def test_module_lesson_relationship(self):
        # Test that Lessons can be associated with a Module and retrieved correctly
        module = Module.objects.create(name='Module 1')
        lesson1 = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        lesson2 = Lesson.objects.create(name='Lesson 2', lesson_type='video')
        module.lessons.add(lesson1, lesson2)

        self.assertEqual(module.lessons.count(), 2, "Module should have two lessons.")
        self.assertIn(lesson1, module.lessons.all(), "Module should contain 'Lesson 1'.")
        self.assertIn(lesson2, module.lessons.all(), "Module should contain 'Lesson 2'.")

    def test_module_not_deleted_with_path(self):
        # Test that deleting a Path does not delete its associated Modules
        module = Module.objects.create(name='Module 1')
        path = Path.objects.create(name='Path 1')
        path.modules.add(module)
        path.delete()

        self.assertEqual(Module.objects.count(), 1, "Module should not be deleted when Path is deleted.")

    def test_lesson_not_deleted_with_module(self):
        # Test that deleting a Module does not delete its associated Lessons
        module = Module.objects.create(name='Module 1')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        module.lessons.add(lesson)
        module.delete()

        self.assertEqual(Lesson.objects.count(), 1, "Lesson should not be deleted when Module is deleted.")
        self.assertFalse(module in lesson.modules.all(), "Lesson should no longer be linked to a deleted Module.")
