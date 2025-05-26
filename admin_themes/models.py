from django.db import models
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class AdminTheme(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="A unique name for the theme.")


    css_url = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="URL to the custom CSS file for this theme. Must be a valid URL."
    )
    js_url = models.URLField(
        blank=True,
        null=True,
        validators=[URLValidator()],
        help_text="URL to the custom JavaScript file for this theme. Must be a valid URL."
    )

    is_active = models.BooleanField(default=False, help_text="Only one theme can be active at a time.")

    # You might add fields for AI suggestions later
    accessibility_suggestions = models.JSONField(blank=True, null=True, default=list, help_text="AI-generated accessibility suggestions.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        # Custom validation: ensure CSS/JS URLs end with appropriate extensions
        if self.css_url and not (self.css_url.endswith('.css') or '.css?' in self.css_url):
            raise ValidationError({'css_url': 'CSS URL must end with .css'})
        if self.js_url and not (self.js_url.endswith('.js') or '.js?' in self.js_url):
            raise ValidationError({'js_url': 'JS URL must end with .js'})

        # Ensure only one theme is active
        if self.is_active:
            # Check for existing active themes, excluding the current instance if it's being updated
            if AdminTheme.objects.filter(is_active=True).exclude(pk=self.pk).exists():
                raise ValidationError('Only one AdminTheme can be active at a time. Deactivate the current theme first.')

    def save(self, *args, **kwargs):
        self.full_clean() # Call full_clean to run field and model-level validation (including custom clean)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Admin Theme"
        verbose_name_plural = "Admin Themes"