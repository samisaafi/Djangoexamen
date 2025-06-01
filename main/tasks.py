# admin_themes/tasks.py
import subprocess
from celery import shared_task
from django.conf import settings
import os
import shutil

# Import AdminTheme here once for both tasks
from .models import AdminTheme


@shared_task
def compile_scss_and_deploy_assets(theme_id):
    """
    Celery task to compile SCSS to CSS and deploy JS assets for a given theme.
    """
    try:
        theme = AdminTheme.objects.get(pk=theme_id)
    except AdminTheme.DoesNotExist:
        print(f"Theme with ID {theme_id} not found for asset deployment.")
        return {"status": "error", "message": f"Theme {theme_id} not found."}

    print(f"Compiling and deploying assets for theme: {theme.name} (PK: {theme_id})...")

    # --- SCSS Compilation (Simulated) ---
    theme_source_dir = os.path.join(settings.MEDIA_ROOT, 'admin_themes_source', theme.name.lower().replace(' ', '_'))
    scss_file = os.path.join(theme_source_dir, 'style.scss')

    css_output_dir = os.path.join(settings.MEDIA_ROOT, 'admin_themes', 'css')
    os.makedirs(css_output_dir, exist_ok=True)
    compiled_css_file = os.path.join(css_output_dir, f'{theme.name.lower().replace(" ', '_")}.css')

    if os.path.exists(scss_file):
        try:
            # Simulate SCSS compilation. In a real scenario, you'd use a library like 'libsass'
            # or call an external 'sass' command here.
            # Example using a simulated write:
            with open(compiled_css_file, 'w') as f:
                f.write(f"/* Compiled CSS for {theme.name} */\n")
                f.write(f"body {{ background-color: {'lightblue' if 'light' in theme.name.lower() else 'darkgray'}; color: {'black' if 'light' in theme.name.lower() else 'white'}; }}\n")
                f.write(f".app-header {{ border-bottom: 2px solid {'#f0f0f0' if 'light' in theme.name.lower() else '#333'}; }}\n")

            theme.css_url = f"{settings.MEDIA_URL}admin_themes/css/{os.path.basename(compiled_css_file)}"
            theme.save(update_fields=['css_url'])
            print(f"Successfully compiled (simulated) SCSS for theme {theme.name}. CSS URL: {theme.css_url}")

        except Exception as e: # Catching general Exception for simplicity here
            print(f"Error compiling SCSS for theme {theme.name}: {e}")
            return {"status": "error", "message": f"SCSS compilation failed: {e}"}
    else:
        print(f"No SCSS file found at {scss_file} for theme {theme.name}. Skipping SCSS compilation.")

    # --- JS Deployment ---
    js_source_file = os.path.join(theme_source_dir, 'script.js')
    js_output_dir = os.path.join(settings.MEDIA_ROOT, 'admin_themes', 'js')
    os.makedirs(js_output_dir, exist_ok=True)
    deployed_js_file = os.path.join(js_output_dir, f'{theme.name.lower().replace(" ', '_")}.js')

    if os.path.exists(js_source_file):
        try:
            shutil.copy(js_source_file, deployed_js_file)
            theme.js_url = f"{settings.MEDIA_URL}admin_themes/js/{os.path.basename(deployed_js_file)}"
            theme.save(update_fields=['js_url'])
            print(f"Successfully deployed JS for theme {theme.name}. JS URL: {theme.js_url}")
        except Exception as e:
            print(f"Error deploying JS for theme {theme.name}: {e}")
            return {"status": "error", "message": f"JS deployment failed: {e}"}
    else:
        print(f"No JS file found at {js_source_file} for theme {theme.name}. Skipping JS deployment.")

    print(f"Asset deployment task finished for theme {theme.name}.")
    return {"status": "success", "message": "Assets compiled and deployed."}


@shared_task
def analyze_theme_for_accessibility(theme_pk):
    try:
        theme = AdminTheme.objects.get(pk=theme_pk)
        print(f"Analyzing theme '{theme.name}' for accessibility...")
        suggestions = []
        css_content = ""

        if theme.css_url:
            try:
                response = requests.get(theme.css_url)
                response.raise_for_status()
                css_content = response.text
            except requests.RequestException as e:
                print(f"Failed to fetch CSS for analysis: {e}")
                suggestions.append("Unable to fetch CSS for accessibility analysis.")

        if css_content:
            if "background-color: black" in css_content and "color: black" in css_content:
                suggestions.append("Low contrast detected: black text on black background.")
            if "font-size: 10px" in css_content:
                suggestions.append("Font size too small (10px); consider increasing to at least 16px for readability.")
        else:
            suggestions.append("No CSS content available for analysis.")

        theme.accessibility_suggestions = "\n".join(suggestions) if suggestions else "No accessibility issues detected."
        theme.save()
    except AdminTheme.DoesNotExist:
        print(f"Theme with PK {theme_pk} not found.")