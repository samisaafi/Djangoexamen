from django.contrib import admin
from .models import Course, Student, Tutor, Enrollment, Profile, Location, AdminTheme
from .tasks import compile_scss_and_deploy_assets, analyze_theme_for_accessibility

from testp.admin_site import custom_admin_site
# Register existing models with the custom admin site
@admin.register(Course, site=custom_admin_site)
class CourseAdmin(admin.ModelAdmin):
    pass

@admin.register(Student, site=custom_admin_site)
class StudentAdmin(admin.ModelAdmin):
    pass

@admin.register(Tutor, site=custom_admin_site)
class TutorAdmin(admin.ModelAdmin):
    pass

@admin.register(Enrollment, site=custom_admin_site)
class EnrollmentAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile, site=custom_admin_site)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    pass

# Moved from admin_themes
@admin.register(AdminTheme)
class AdminThemeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            AdminTheme.objects.filter(is_active=True).exclude(pk=obj.pk).update(is_active=False)
        super().save_model(request, obj, form, change)
        if obj.is_active:
            compile_scss_and_deploy_assets.delay(obj.pk)
            analyze_theme_for_accessibility.delay(obj.pk)

    def activate_selected_themes(self, request, queryset):
        if queryset.count() > 1:
            self.message_user(request, "Only one theme can be activated at a time. Please select only one.", level='error')
            return

        theme_to_activate = queryset.first()
        if theme_to_activate:
            AdminTheme.objects.filter(is_active=True).exclude(pk=theme_to_activate.pk).update(is_active=False)
            theme_to_activate.is_active = True
            theme_to_activate.save()
            self.message_user(request, f"Theme '{theme_to_activate.name}' has been activated.")
    activate_selected_themes.short_description = "Activate selected admin theme"