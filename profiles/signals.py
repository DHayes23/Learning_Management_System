from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from content.models import Path, Module, Lesson, StudentProgress
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

@receiver(m2m_changed, sender=Profile.assigned_paths.through)
def update_student_progress_for_assigned_paths(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        if not reverse:  # Adding paths to a student
            profile = instance
            path_ids = pk_set
            for path_id in path_ids:
                path = Path.objects.get(pk=path_id)
                for module in path.modules.all():
                    for lesson in module.lessons.all():
                        StudentProgress.objects.get_or_create(
                            student=profile.user,
                            lesson=lesson,
                            defaults={'completed': False}
                        )
        else:  # Adding students to a path
            path = instance
            user_ids = pk_set
            for user_id in user_ids:
                user = User.objects.get(pk=user_id)
                for module in path.modules.all():
                    for lesson in module.lessons.all():
                        StudentProgress.objects.get_or_create(
                            student=user,
                            lesson=lesson,
                            defaults={'completed': False}
                        )

    elif action == "post_remove":
        if not reverse:  # Removing paths from a student
            profile = instance
            path_ids = pk_set
            for path_id in path_ids:
                path = Path.objects.get(pk=path_id)
                for module in path.modules.all():
                    for lesson in module.lessons.all():
                        other_paths_with_lesson = profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not other_paths_with_lesson:
                            StudentProgress.objects.filter(
                                student=profile.user,
                                lesson=lesson
                            ).delete()
        else:  # Removing students from a path
            path = instance
            user_ids = pk_set
            for user_id in user_ids:
                user = User.objects.get(pk=user_id)
                for module in path.modules.all():
                    for lesson in module.lessons.all():
                        other_paths_with_lesson = user.profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not other_paths_with_lesson:
                            StudentProgress.objects.filter(
                                student=user,
                                lesson=lesson
                            ).delete()

@receiver(m2m_changed, sender=Module.lessons.through)
def update_student_progress_for_lessons_in_module(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        if not reverse:  # Adding lessons to the module
            module = instance
            lesson_ids = pk_set
            for lesson_id in lesson_ids:
                lesson = Lesson.objects.get(pk=lesson_id)
                for path in module.paths.all():
                    for student in path.students.all():
                        StudentProgress.objects.get_or_create(
                            student=student.user,
                            lesson=lesson,
                            defaults={'completed': False}
                        )
        else:  # Adding modules to a lesson
            lesson = instance
            module_ids = pk_set
            for module_id in module_ids:
                module = Module.objects.get(pk=module_id)
                for path in module.paths.all():
                    for student in path.students.all():
                        StudentProgress.objects.get_or_create(
                            student=student.user,
                            lesson=lesson,
                            defaults={'completed': False}
                        )

    elif action == "post_remove":
        if not reverse:  # Removing lessons from the module
            module = instance
            lesson_ids = pk_set
            for lesson_id in lesson_ids:
                lesson = Lesson.objects.get(pk=lesson_id)
                for path in module.paths.all():
                    for student in path.students.all():
                        # Check if the lesson is still part of any other modules in the assigned paths
                        still_assigned = student.user.profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not still_assigned:
                            StudentProgress.objects.filter(
                                student=student.user,
                                lesson=lesson
                            ).delete()
        else:  # Removing modules from a lesson
            lesson = instance
            module_ids = pk_set
            for module_id in module_ids:
                module = Module.objects.get(pk=module_id)
                for path in module.paths.all():
                    for student in path.students.all():
                        still_assigned = student.user.profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not still_assigned:
                            StudentProgress.objects.filter(
                                student=student.user,
                                lesson=lesson
                            ).delete()

@receiver(m2m_changed, sender=Path.modules.through)
def update_student_progress_for_modules_in_path(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        if not reverse:  # Adding modules to the path
            path = instance
            module_ids = pk_set
            for module_id in module_ids:
                module = Module.objects.get(pk=module_id)
                for student in path.students.all():
                    for lesson in module.lessons.all():
                        StudentProgress.objects.get_or_create(
                            student=student.user,
                            lesson=lesson,
                            defaults={'completed': False}
                        )

    elif action == "post_remove":
        if not reverse:  # Removing modules from the path
            path = instance
            module_ids = pk_set
            for module_id in module_ids:
                module = Module.objects.get(pk=module_id)
                for student in path.students.all():
                    for lesson in module.lessons.all():
                        still_assigned = student.user.profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not still_assigned:
                            StudentProgress.objects.filter(
                                student=student.user,
                                lesson=lesson
                            ).delete()
        else:  # Removing paths from a module
            module = instance
            path_ids = pk_set
            for path_id in path_ids:
                path = Path.objects.get(pk=path_id)
                for student in path.students.all():
                    for lesson in module.lessons.all():
                        still_assigned = student.user.profile.assigned_paths.filter(modules__lessons=lesson).exists()
                        if not still_assigned:
                            StudentProgress.objects.filter(
                                student=student.user,
                                lesson=lesson
                            ).delete()
