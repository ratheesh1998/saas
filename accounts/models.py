from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
import secrets

class User(AbstractUser):
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.email


class RailwaySettings(models.Model):
    """Store Railway.app credentials for each user"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='railway_settings'
    )
    railway_template_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Template ID"
    )
    railway_workspace_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Workspace ID"
    )
    railway_token = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Railway API Token"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Railway Settings"
        verbose_name_plural = "Railway Settings"
    
    def __str__(self):
        return f"Railway Settings for {self.user.email}"


class Template(models.Model):
    """Store Railway templates created by users"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='templates'
    )
    name = models.CharField(
        max_length=255,
        help_text="Template name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Template description"
    )
    template_config = models.JSONField(
        default=dict,
        help_text="Template configuration (JSON)"
    )
    railway_template_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Template ID (if created on Railway)"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is active"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"

