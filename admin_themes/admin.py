# admin_themes/admin.py
from django.contrib import admin
from .models import AdminTheme
from .tasks import compile_scss_and_deploy_assets, analyze_theme_for_accessibility

# Import your custom admin site instance
from testp.admin_site import custom_admin_site # <--- IMPORTANT: Adjust 'testp' if your project name is different

# Unregister from the default admin.site first (if it was registered via @admin.register)
try:
    admin.site.unregister(AdminTheme)
except admin.sites.NotRegistered:
    pass # Already unregistered or never registered

@admin.register(AdminTheme, site=custom_admin_site) # Register with your custom admin site
class AdminThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'css_url', 'js_url', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
    actions = ['activate_selected_themes']

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