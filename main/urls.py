from django.urls import path
from . import views

urlpatterns = [
    path('themes/', views.AdminThemeListCreateView.as_view(), name='theme-list-create'),
    path('themes/<int:pk>/apply/', views.ApplyAdminThemeView.as_view(), name='apply-theme'),
]