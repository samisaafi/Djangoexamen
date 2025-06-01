from .models import AdminTheme

def active_admin_theme(request):
    try:
        theme = AdminTheme.objects.get(is_active=True)
    except AdminTheme.DoesNotExist:
        theme = None
    return {'active_admin_theme': theme}