from django.contrib import admin
from .models import Path, Module, Lesson, StudentProgress

class ModuleAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name', 'description')
    filter_horizontal = ('lessons',)

class PathAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson_type', 'get_modules')
    list_filter = ('lesson_type',)

    def get_modules(self, obj):
        return ", ".join([module.name for module in obj.modules.all()])
    get_modules.short_description = 'Modules'

class StudentProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'completed', 'date_completed')
    list_filter = ('student', 'completed')
    search_fields = ('student__username', 'lesson__name')

admin.site.register(Path, PathAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentProgress, StudentProgressAdmin)
