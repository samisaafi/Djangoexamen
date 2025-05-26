# admin_themes/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminThemeViewSet

router = DefaultRouter()
router.register(r'', AdminThemeViewSet, basename='admin-themes') # Register AdminThemeViewSet at root of this app's URL

urlpatterns = [
    path('', include(router.urls)),
]