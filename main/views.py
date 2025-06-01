from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from .models import AdminTheme
from .serializers import AdminThemeSerializer
from .tasks import compile_scss_and_deploy_assets, analyze_theme_for_accessibility

class AdminThemeListCreateView(generics.ListCreateAPIView):
    queryset = AdminTheme.objects.all()
    serializer_class = AdminThemeSerializer
    permission_classes = [permissions.IsAdminUser]

class ApplyAdminThemeView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        try:
            theme = AdminTheme.objects.get(pk=pk)
        except AdminTheme.DoesNotExist:
            return Response({"error": "AdminTheme not found"}, status=404)

        AdminTheme.objects.filter(is_active=True).exclude(pk=theme.pk).update(is_active=False)
        theme.is_active = True
        theme.save()

        compile_scss_and_deploy_assets.delay(theme.pk)
        analyze_theme_for_accessibility.delay(theme.pk)

        return Response(AdminThemeSerializer(theme).data)