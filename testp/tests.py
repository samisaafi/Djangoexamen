from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from graphene_dDryRun import APIRequestFactory
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenClient
from main.models import AdminTheme
from main.schema import schema
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from datetime import datetime
import os

class AdminThemeTests(TestCase):
    def setUp(self):
        # Create a superuser
        self.superuser = User.objects.create_superuser(username='sami', password='sami', email='')
        self.client = APIClient()
        self.client.login(username='sami', password='sami1')


        # Create a test theme
        self.theme = AdminTheme.objects.create(
            name="Test Theme",
            css_url="http://example.com/style.css",
            js_url="http://example.com/script.js",
            is_active=False,
            created_at=datetime.now()
        )

        # GraphQL client for testing mutations
        self.graphql_client = JSONWebTokenClient(schema=schema)
        self.graphql_client.authenticate(self.superuser)

    def test_model_validation_css_url(self):
        # Test invalid CSS URL
        invalid_theme = AdminTheme(
            name="Invalid CSS Theme",
            css_url="http://example.com/style.txt",  # Wrong extension
            js_url="http://example.com/script.js"
        )
        with self.assertRaisesMessage(Exception, "CSS URL must end with .css"):
            invalid_theme.clean()

    def test_model_validation_missing_css_and_scss(self):
        # Test missing CSS URL and SCSS file
        invalid_theme = AdminTheme(
            name="Missing CSS Theme",
            js_url="http://example.com/script.js"
        )
        with self.assertRaisesMessage(Exception, "Either a CSS URL or an SCSS file must be provided."):
            invalid_theme.clean()

    def test_rest_endpoint_create_theme(self):
        # Test creating a theme via REST API
        data = {
            "name": "New Theme",
            "css_url": "http://example.com/new_style.css",
            "js_url": "http://example.com/new_script.js"
        }
        response = self.client.post(reverse('theme-list-create'), data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(AdminTheme.objects.count(), 2)
        self.assertEqual(response.data['name'], "New Theme")

    def test_rest_endpoint_apply_theme(self):
        # Test applying a theme via REST API
        response = self.client.post(reverse('apply-theme', args=[self.theme.id]))
        self.assertEqual(response.status_code, 200)
        self.theme.refresh_from_db()
        self.assertTrue(self.theme.is_active)

    def test_rest_endpoint_unauthorized(self):
        # Test access by non-superuser
        response = self.regular_client.post(reverse('apply-theme', args=[self.theme.id]))
        self.assertEqual(response.status_code, 403)

    def test_graphql_mutation_apply_theme(self):
        # Test applying a theme via GraphQL mutation
        mutation = """
            mutation ApplyAdminTheme($id: Int!) {
                applyAdminTheme(id: $id) {
                    id
                    isActive
                }
            }
        """
        response = self.graphql_client.execute(mutation, variables={'id': self.theme.id})
        self.assertIsNone(response.errors)
        self.theme.refresh_from_db()
        self.assertTrue(self.theme.is_active)

    def test_graphql_mutation_unauthorized(self):
        # Test GraphQL mutation access by non-superuser
        unauthorized_client = JSONWebTokenClient(schema=schema)
        unauthorized_client.authenticate(self.regular_user)
        mutation = """
            mutation ApplyAdminTheme($id: Int!) {
                applyAdminTheme(id: $id) {
                    id
                    isActive
                }
            }
        """
        response = unauthorized_client.execute(mutation, variables={'id': self.theme.id})
        self.assertIsNotNone(response.errors)
        self.assertIn("permission", str(response.errors).lower())

    def test_celery_task_compile_scss(self):
        # Test SCSS compilation task
        from main.tasks import compile_scss_and_deploy_assets
        theme = AdminTheme.objects.create(
            name="SCSS Theme",
            scss_file=SimpleUploadedFile("style.scss", b"body { background-color: lightblue; }"),
            js_url="http://example.com/script.js"
        )
        result = compile_scss_and_deploy_assets(theme.id)
        self.assertEqual(result['status'], 'success')
        theme.refresh_from_db()
        self.assertTrue(theme.css_url.endswith('.css'))

    def test_celery_task_accessibility_analysis(self):
        # Test accessibility analysis task
        from main.tasks import analyze_theme_for_accessibility
        theme = AdminTheme.objects.create(
            name="Accessibility Theme",
            css_url="http://example.com/invalid.css",  # Simulate inaccessible CSS
            js_url="http://example.com/script.js"
        )
        analyze_theme_for_accessibility(theme.id)
        theme.refresh_from_db()
        self.assertIn("Unable to fetch CSS", theme.accessibility_suggestions)