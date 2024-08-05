from django.contrib import admin
from .models import Path, Module, Lesson, StudentProgress

class ModuleAdmin(admin.ModelAdmin):
    filter_horizontal = ('lessons',)
    search_fields = ('name',)
    list_display = ('name', 'description')

class PathAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)

class LessonAdmin(admin.ModelAdmin):
    list_display = ('name', 'lesson_type', 'get_modules')
    list_filter = ('lesson_type',)

    def get_modules(self, obj):
        return ", ".join([module.name for module in obj.modules.all()])
    get_modules.short_description = 'Modules'

admin.site.register(Path, PathAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(StudentProgress)
