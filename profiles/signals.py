from django.db.models.signals import post_save, pre_delete, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from content.models import Path, Module, Lesson, StudentProgress
from .badges import BADGES
from .models import Profile
from django.db.models import Sum
from django.utils import timezone

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
                            recalculate_profile_points(profile)
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
                            recalculate_profile_points(user.profile)

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
                            recalculate_profile_points(student.user.profile)
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
                            recalculate_profile_points(student.user.profile)

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
                            recalculate_profile_points(student.user.profile)
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
                            recalculate_profile_points(student.user.profile)

@receiver(pre_delete, sender=Module)
def delete_student_progress_for_deleted_module(sender, instance, **kwargs):
    # Delete StudentProgress for lessons in the module that is about to be deleted,
    # only if those lessons are not associated with other modules assigned to the student.
    lessons = instance.lessons.all()
    for lesson in lessons:
        # Find all students who have progress in this lesson
        student_progress_qs = StudentProgress.objects.filter(lesson=lesson)
        for student_progress in student_progress_qs:
            student = student_progress.student
            # Check if this lesson is part of any other modules assigned to the student's paths
            overlapping_modules = Module.objects.filter(
                lessons=lesson,
                paths__students__user=student
            ).exclude(id=instance.id).exists()

            if not overlapping_modules:
                # Delete the progress record if this lesson is not part of any other assigned modules
                student_progress.delete()
                recalculate_profile_points(student.profile)

@receiver(pre_delete, sender=Path)
def delete_student_progress_for_deleted_path(sender, instance, **kwargs):
    # Delete StudentProgress for lessons in the modules of the path that is about to be deleted,
    # only if those lessons are not associated with other modules in other paths assigned to the student.
    modules = instance.modules.all()
    for module in modules:
        lessons = module.lessons.all()
        for lesson in lessons:
            # Find all students who have progress in this lesson
            student_progress_qs = StudentProgress.objects.filter(lesson=lesson)
            for student_progress in student_progress_qs:
                student = student_progress.student
                # Check if this lesson is part of any other paths assigned to the student
                overlapping_paths = student.profile.assigned_paths.filter(
                    modules__lessons=lesson
                ).exclude(id=instance.id).exists()

                if not overlapping_paths:
                    # Delete the progress record if this lesson is not part of any other assigned paths
                    student_progress.delete()
                    recalculate_profile_points(student.profile)

@receiver(pre_delete, sender=Lesson)
def update_points_on_lesson_deletion(sender, instance, **kwargs):
    # Find all students who have progress in this lesson
    student_progress_qs = StudentProgress.objects.filter(lesson=instance)
    for student_progress in student_progress_qs:
        student = student_progress.student
        # Delete the progress entry for the lesson being deleted
        student_progress.delete()
        recalculate_profile_points(student.profile)

@receiver(pre_delete, sender=StudentProgress)
def update_points_on_student_progress_deletion(sender, instance, **kwargs):
    # Recalculate the student's total points when a StudentProgress record is deleted
    recalculate_profile_points(instance.student.profile)

@receiver(post_save, sender=StudentProgress)
def update_points_on_completion(sender, instance, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    if instance.completed:
        if instance.points != instance.lesson.points:
            instance.points = instance.lesson.points
            instance.save(update_fields=['points'])

        # Update daily streak
        instance.student.profile.update_daily_streak()
    else:
        if instance.points != 0:
            instance.points = 0
            instance.save(update_fields=['points'])

@receiver(post_save, sender=StudentProgress)
def update_student_profile_points(sender, instance, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    recalculate_profile_points(instance.student.profile)

@receiver(post_save, sender=StudentProgress)
def update_date_completed_on_completion(sender, instance, **kwargs):
    if 'raw' in kwargs and kwargs['raw']:
        return

    if instance.completed and not instance.date_completed:
        instance.date_completed = timezone.now()
        instance.save(update_fields=['date_completed'])
    elif not instance.completed and instance.date_completed:
        instance.date_completed = None
        instance.save(update_fields=['date_completed'])

def recalculate_profile_points(profile):
    total_points = StudentProgress.objects.filter(student=profile.user, completed=True).aggregate(Sum('points'))['points__sum'] or 0
    profile.points = total_points
    profile.save(update_fields=['points'])

    # Check and award badges
    for badge in BADGES:
        if badge['condition'](profile):
            profile.award_badge(badge['name'])
