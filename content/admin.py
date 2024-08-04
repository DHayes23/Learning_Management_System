from django.contrib import admin
from .models import Path, Module, Lesson

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class ModuleAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

class PathAdmin(admin.ModelAdmin):
    filter_horizontal = ('modules',)

admin.site.register(Path, PathAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Lesson)
