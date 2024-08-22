from django.test import TestCase
from .models import Path, Module, Lesson, Question

class ContentModelTest(TestCase):
    
    def test_path_creation(self):
        # Test that a path is correctly created
        path = Path.objects.create(name='Path 1', description='Test Path')
        self.assertEqual(path.name, 'Path 1', "Path should be created with the correct name.")
        self.assertEqual(Path.objects.count(), 1, "There should be one Path in the database.")

    def test_unique_path_name(self):
        # Test that creating two paths with the same name raises an error
        Path.objects.create(name='Path 1')
        with self.assertRaises(Exception):
            Path.objects.create(name='Path 1')

    def test_module_creation(self):
        # Test that a module is correctly created
        module = Module.objects.create(name='Module 1', description='Test Module')
        self.assertEqual(module.name, 'Module 1', "Module should be created with the correct name.")
        self.assertEqual(Module.objects.count(), 1, "There should be one Module in the database.")

    def test_unique_module_name(self):
        # Test that creating two modules with the same name raises an error
        Module.objects.create(name='Module 1')
        with self.assertRaises(Exception):
            Module.objects.create(name='Module 1')

    def test_lesson_creation(self):
        # Test that a lesson is correctly created
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.assertEqual(lesson.name, 'Lesson 1', "Lesson should be created with the correct name.")
        self.assertEqual(Lesson.objects.count(), 1, "There should be one Lesson in the database.")

    def test_unique_lesson_name(self):
        # Test that creating two lessons with the same name raises an error
        Lesson.objects.create(name='Lesson 1')
        with self.assertRaises(Exception):
            Lesson.objects.create(name='Lesson 1')

    def test_time_to_complete_verbose_name(self):
        # Test that the time_to_complete field has the correct verbose name
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text', time_to_complete=15)
        field_label = lesson._meta.get_field('time_to_complete').verbose_name
        self.assertEqual(field_label, 'Time to Complete (Minutes)', "The verbose name should be 'Time to Complete (Minutes)'.")

    def test_optional_sub_lesson_fields(self):
        # Test that optional fields for sub-lesson types can be left blank
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='quiz')
        self.assertIsNone(lesson.video_url, "Video URL should be None for a lesson without video content.")
        self.assertEqual(lesson.quiz_questions.count(), 0, "Quiz questions should be empty for a newly created quiz lesson.")
        self.assertIsNone(lesson.due_date, "Due date should be None for a lesson without a deliverable.")
        self.assertIsNone(lesson.recipient_email, "Recipient email should be None for a lesson without a deliverable.")

    def test_path_module_relationship(self):
        # Test the relationship between paths and modules
        path = Path.objects.create(name='Path 1')
        module1 = Module.objects.create(name='Module 1')
        module2 = Module.objects.create(name='Module 2')
        path.modules.add(module1, module2)

        self.assertEqual(path.modules.count(), 2, "Path should have two modules.")
        self.assertIn(module1, path.modules.all(), "Path should contain 'Module 1'.")
        self.assertIn(module2, path.modules.all(), "Path should contain 'Module 2'.")

    def test_module_lesson_relationship(self):
        # Test the relationship between modules and lessons
        module = Module.objects.create(name='Module 1')
        lesson1 = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        lesson2 = Lesson.objects.create(name='Lesson 2', lesson_type='video')
        module.lessons.add(lesson1, lesson2)

        self.assertEqual(module.lessons.count(), 2, "Module should have two lessons.")
        self.assertIn(lesson1, module.lessons.all(), "Module should contain 'Lesson 1'.")
        self.assertIn(lesson2, module.lessons.all(), "Module should contain 'Lesson 2'.")

    def test_module_not_deleted_with_path(self):
        # Test that deleting a path does not delete its modules
        module = Module.objects.create(name='Module 1')
        path = Path.objects.create(name='Path 1')
        path.modules.add(module)
        path.delete()

        self.assertEqual(Module.objects.count(), 1, "Module should not be deleted when Path is deleted.")

    def test_lesson_not_deleted_with_module(self):
        # Test that deleting a module does not delete its lessons
        module = Module.objects.create(name='Module 1')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        module.lessons.add(lesson)
        module.delete()

        self.assertEqual(Lesson.objects.count(), 1, "Lesson should not be deleted when Module is deleted.")
        self.assertEqual(lesson.modules.count(), 0, "Lesson should not be associated with any module after the module is deleted.")

    def test_lesson_can_be_added_to_multiple_modules(self):
        # Test that a lesson can be added to multiple modules
        module1 = Module.objects.create(name='Module 1')
        module2 = Module.objects.create(name='Module 2')
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        module1.lessons.add(lesson)
        module2.lessons.add(lesson)

        self.assertIn(lesson, module1.lessons.all(), "Lesson should be in Module 1.")
        self.assertIn(lesson, module2.lessons.all(), "Lesson should be in Module 2.")
        self.assertEqual(lesson.modules.count(), 2, "Lesson should be associated with two modules.")

    def test_lesson_without_quiz_questions(self):
        # Test that a lesson of type quiz without questions handles the case gracefully
        lesson = Lesson.objects.create(name='Lesson Quiz', lesson_type='quiz', passing_percentage=70)
        self.assertEqual(lesson.quiz_questions.count(), 0, "Quiz should start with no questions.")
        self.assertFalse(lesson.quiz_questions.exists(), "No questions should be linked to the quiz lesson initially.")

    def test_question_creation(self):
        # Test the creation of a question and its string representation
        question = Question.objects.create(
            question_text="What is the capital of France?",
            correct_answer="Paris",
            incorrect_answer_1="Berlin",
            incorrect_answer_2="Rome",
            incorrect_answer_3="Madrid"
        )
        self.assertEqual(str(question), "What is the capital of France?", "Question should be created with the correct text.")
        self.assertEqual(question.correct_answer, "Paris", "Correct answer should be 'Paris'.")

    def test_lesson_difficulty_level(self):
        # Test that the difficulty level is set correctly and defaults to 'medium'
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.assertEqual(lesson.difficulty, 'medium', "The default difficulty level should be 'medium'.")
        lesson.difficulty = 'hard'
        lesson.save()
        self.assertEqual(lesson.difficulty, 'hard', "The difficulty level should be updated to 'hard'.")

    def test_path_str_representation(self):
        # Test the string representation of the Path model
        path = Path.objects.create(name='Path 1')
        self.assertEqual(str(path), 'Path 1', "Path __str__ should return the path name.")

    def test_module_str_representation(self):
        # Test the string representation of the Module model
        module = Module.objects.create(name='Module 1')
        self.assertEqual(str(module), 'Module 1', "Module __str__ should return the module name.")

    def test_lesson_str_representation(self):
        # Test the string representation of the Lesson model
        lesson = Lesson.objects.create(name='Lesson 1', lesson_type='text')
        self.assertEqual(str(lesson), 'Lesson 1 (Text Based)', "Lesson __str__ should return the lesson name and type.")
