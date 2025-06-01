from rest_framework import serializers
from .models import AdminTheme

class AdminThemeSerializer(serializers.ModelSerializer):
    scss_file = serializers.FileField(required=False, allow_null=True)
    js_file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = AdminTheme
        fields = ['id', 'name', 'css_url', 'js_url', 'scss_file', 'js_file', 'is_active', 'created_at', 'accessibility_suggestions']