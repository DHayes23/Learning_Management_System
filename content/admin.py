from django.contrib import admin
from .models import Path, Module, Lesson, Question, StudentProgress

class ModuleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description')
    filter_horizontal = ('lessons',)

class PathAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson_type', 'get_modules', 'points', 'difficulty', 'time_to_complete')
    list_filter = ('lesson_type', 'difficulty')

    filter_horizontal = ('quiz_questions',)

    def get_modules(self, obj):
        return ", ".join([module.name for module in obj.modules.all()])
    get_modules.short_description = 'Modules'

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {
                'fields': ('name', 'points', 'difficulty', 'time_to_complete', 'description', 'lesson_type', 'content')
            }),
            ('Video Options', {
                'fields': ('video_url',),
                'classes': ('collapse',)
            }),
            ('Quiz Options', {
                'fields': ('quiz_questions', 'passing_percentage'),
                'classes': ('collapse',)
            }),
            ('Deliverable Options', {
                'fields': ('due_date', 'recipient_email'),
                'classes': ('collapse',)
            }),
        ]
        return fieldsets

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['video_url'].required = False
            form.base_fields['quiz_questions'].required = False
            form.base_fields['passing_percentage'].required = False
            form.base_fields['due_date'].required = False
            form.base_fields['recipient_email'].required = False
        return form

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text',)
    search_fields = ('question_text',)

class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'date_completed')
    list_filter = ('student', 'completed')
    search_fields = ('student__username', 'lesson__name')

admin.site.register(Path, PathAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(StudentProgress, StudentProgressAdmin)
