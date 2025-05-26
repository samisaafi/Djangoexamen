# DJANGO_DS_MAIN/admin_site.py
from django.contrib.admin import AdminSite
from admin_themes.models import AdminTheme # Import your theme model

class CustomAdminSite(AdminSite):
    site_header = "Custom Django Admin"
    site_title = "My Admin Portal"
    index_title = "Admin Panel"

    def each_context(self, request):
        context = super().each_context(request)
        try:
            context['active_admin_theme'] = AdminTheme.objects.get(is_active=True)
        except AdminTheme.DoesNotExist:
            context['active_admin_theme'] = None # No active theme
        return context

# Instantiate your custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

# Register models here if you want to use this site for all your models
# from main.models import YourMainModel # Example
# custom_admin_site.register(YourMainModel)
# custom_admin_site.register(AdminTheme, AdminThemeAdmin) # If you want to use your custom admin for themes too