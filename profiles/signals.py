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
        profile = instance if not reverse else User.objects.get(pk=list(pk_set)[0]).profile
        path_ids = pk_set if not reverse else [instance.pk]
        
        for path_id in path_ids:
            path = Path.objects.get(pk=path_id)
            for module in path.modules.all():
                for lesson in module.lessons.all():
                    StudentProgress.objects.get_or_create(
                        student=profile.user,
                        lesson=lesson,
                        defaults={'completed': False}
                    )

    elif action == "post_remove":
        profile = instance if not reverse else User.objects.get(pk=list(pk_set)[0]).profile
        path_ids = pk_set if not reverse else [instance.pk]

        for path_id in path_ids:
            path = Path.objects.get(pk=path_id)
            for module in path.modules.all():
                StudentProgress.objects.filter(
                    student=profile.user,
                    lesson__in=module.lessons.all()
                ).delete()

@receiver(m2m_changed, sender=Module.lessons.through)
def update_student_progress_for_lessons(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        module = instance if not reverse else Module.objects.get(pk=list(pk_set)[0])
        lesson_ids = pk_set if not reverse else [instance.pk]

        for lesson_id in lesson_ids:
            lesson = Lesson.objects.get(pk=lesson_id)
            for path in module.paths.all():
                for student in path.students.all():
                    StudentProgress.objects.get_or_create(
                        student=student.user,
                        lesson=lesson,
                        defaults={'completed': False}
                    )

    elif action == "post_remove":
        module = instance if not reverse else Module.objects.get(pk=list(pk_set)[0])
        lesson_ids = pk_set if not reverse else [instance.pk]

        for lesson_id in lesson_ids:
            StudentProgress.objects.filter(
                lesson_id=lesson_id
            ).delete()

@receiver(m2m_changed, sender=Path.modules.through)
def update_student_progress_for_modules_in_path(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add":
        path = instance if not reverse else Path.objects.get(pk=list(pk_set)[0])
        module_ids = pk_set if not reverse else [instance.pk]

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
        path = instance if not reverse else Path.objects.get(pk=list(pk_set)[0])
        module_ids = pk_set if not reverse else [instance.pk]

        for module_id in module_ids:
            module = Module.objects.get(pk=module_id)
            for student in path.students.all():
                StudentProgress.objects.filter(
                    student=student.user,
                    lesson__in=module.lessons.all()
                ).delete()

@receiver(m2m_changed, sender=Module.lessons.through)
def update_student_progress_on_lesson_module_change(sender, instance, action, reverse, model, pk_set, **kwargs):
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
                # Delete student progress related to this lesson
                StudentProgress.objects.filter(
                    lesson_id=lesson_id
                ).delete()
        else:  # Removing modules from a lesson
            lesson = instance
            module_ids = pk_set
            for module_id in module_ids:
                # Delete student progress related to this lesson in the module
                StudentProgress.objects.filter(
                    lesson=lesson
                ).delete()