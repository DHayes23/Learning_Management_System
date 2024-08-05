from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile
from content.models import Module, Path

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'cohort', 'assigned_paths_list', 'get_completed_paths_list')
    list_filter = ('role', 'cohort')
    filter_horizontal = ('assigned_paths',)

    def assigned_paths_list(self, obj):
        return ", ".join([path.name for path in obj.assigned_paths.all()])
    assigned_paths_list.short_description = 'Assigned Paths'

    def get_completed_paths_list(self, obj):
        completed_paths = obj.get_completed_paths()
        return ", ".join([path.name for path in completed_paths]) if completed_paths else 'No Paths Completed'
    get_completed_paths_list.short_description = 'Completed Paths'

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'
    filter_horizontal = ('assigned_paths',)

class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
