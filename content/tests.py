from django.test import TestCase
from .models import Path, Module, Lesson

class ContentModelTest(TestCase):
    
    def test_path_creation(self):
        path = Path.objects.create(name='Path 1', description='Test Path')
        self.assertEqual(path.name, 'Path 1', "Path should be created with the correct name.")
        self.assertEqual(Path.objects.count(), 1, "There should be one Path in the database.")

    def test_module_creation(self):
        module = Module.objects.create(name='Module 1', description='Test Module')
        self.assertEqual(module.name, 'Module 1', "Module should be created with the correct name.")
        self.assertEqual(Module.objects.count(), 1, "There should be one Module in the database.")

    def test_lesson_creation(self):
        module = Module.objects.create(name='Module 1')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text', module=module)
        self.assertEqual(lesson.name, 'Lesson 1', "Lesson should be created with the correct name.")
        self.assertEqual(Lesson.objects.count(), 1, "There should be one Lesson in the database.")
        self.assertEqual(lesson.module, module, "Lesson should be correctly linked to its Module.")

    def test_path_module_relationship(self):
        path = Path.objects.create(name='Path 1')
        module1 = Module.objects.create(name='Module 1')
        module2 = Module.objects.create(name='Module 2')
        path.modules.add(module1, module2)

        self.assertEqual(path.modules.count(), 2, "Path should have two modules.")
        self.assertIn(module1, path.modules.all(), "Path should contain 'Module 1'.")
        self.assertIn(module2, path.modules.all(), "Path should contain 'Module 2'.")

    def test_module_lesson_relationship(self):
        module = Module.objects.create(name='Module 1')
        lesson1 = Lesson.objects.create(name='Lesson 1', lesson_type='text', module=module)
        lesson2 = Lesson.objects.create(name='Lesson 2', lesson_type='video', module=module)

        self.assertEqual(module.lessons.count(), 2, "Module should have two lessons.")
        self.assertIn(lesson1, module.lessons.all(), "Module should contain 'Lesson 1'.")
        self.assertIn(lesson2, module.lessons.all(), "Module should contain 'Lesson 2'.")

    def test_module_not_deleted_with_path(self):
        module = Module.objects.create(name='Module 1')
        path = Path.objects.create(name='Path 1')
        path.modules.add(module)
        path.delete()

        self.assertEqual(Module.objects.count(), 1, "Module should not be deleted when Path is deleted.")

    def test_lesson_not_deleted_with_module(self):
        module = Module.objects.create(name='Module 1')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text', module=module)
        module.delete()

        self.assertEqual(Lesson.objects.count(), 1, "Lesson should not be deleted when Module is deleted.")
        self.assertIsNone(Lesson.objects.first().module, "Lesson's module should be set to None when Module is deleted.")
