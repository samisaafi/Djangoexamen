# admin_themes/serializers.py
from rest_framework import serializers
from .models import AdminTheme

class AdminThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminTheme
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'accessibility_suggestions')

    def validate(self, data):
        # Example: Ensure that if a CSS URL is provided, it's not an empty string
        if 'css_url' in data and data['css_url'] == '':
            data['css_url'] = None
        if 'js_url' in data and data['js_url'] == '':
            data['js_url'] = None
        return data