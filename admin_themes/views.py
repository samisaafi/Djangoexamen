from django.shortcuts import render

# Create your views here.
# admin_themes/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated # For security
from django.middleware.csrf import CsrfViewMiddleware # For CSRF protection
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from .models import AdminTheme
from .serializers import AdminThemeSerializer
from .tasks import compile_scss_and_deploy_assets, analyze_theme_for_accessibility

@method_decorator(csrf_protect, name='dispatch') # Apply CSRF protection to the viewset
class AdminThemeViewSet(viewsets.ModelViewSet):
    queryset = AdminTheme.objects.all().order_by('-created_at')
    serializer_class = AdminThemeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] # Ensure user is logged in AND is superuser

    @action(detail=True, methods=['post'], url_path='apply')
    def apply_theme(self, request, pk=None):
        theme = self.get_object() # Gets the specific theme instance by pk

        # Deactivate all other themes
        AdminTheme.objects.filter(is_active=True).exclude(pk=theme.pk).update(is_active=False)

        # Activate the selected theme
        theme.is_active = True
        theme.save()

        compile_scss_and_deploy_assets.delay(theme.pk)

        # Analyze theme for accessibility   
        analyse_theme_for_accessibility.delay(theme.pk)

        serializer = self.get_serializer(theme)
        return Response({
            'status': 'theme applied', 
            'theme_name': theme.name,
            'theme': serializer.data,
            'asset_task_scheduled': True
        }, status=status.HTTP_200_OK)

    # For "upload custom themes" part:
    # If theme files are to be uploaded directly via API, you'd add FileField to model
    # and handle the upload logic here or in the serializer.
    # For now, we assume URLs are provided.