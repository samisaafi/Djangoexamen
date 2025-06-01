from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Custom Admin Panel"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Admin Dashboard"

custom_admin_site = CustomAdminSite(name='customadmin')