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


# =============================================================================
# TEMPLATE - Blueprint/Design for deployments
# =============================================================================

class Template(models.Model):
    """Blueprint/Design for Railway deployments - not actually deployed"""
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
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this template is active"
    )
    is_published = models.BooleanField(
        default=False,
        help_text="Whether this template has been published to Railway"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template"
        verbose_name_plural = "Templates"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"
    
    def publish(self):
        """Create a Project from this Template"""
        # Create Project
        project = Project.objects.create(
            user=self.user,
            source_template=self,
            name=f"{self.name} Deployment",
            description=f"Deployed from template: {self.name}"
        )
        
        # Copy all template services to project services
        for template_service in self.services.all():
            ProjectService.objects.create(
                project=project,
                source_service=template_service,
                service_id=template_service.service_id,
                name=template_service.name,
                image=template_service.image,
                registry_username=template_service.registry_username,
                registry_password=template_service.registry_password,
                cpu=template_service.cpu,
                memory=template_service.memory,
                variables=template_service.variables,
                networking=template_service.networking,
                position_x=template_service.position_x,
                position_y=template_service.position_y
            )
        
        self.is_published = True
        self.save()
        
        return project


class TemplateService(models.Model):
    """Service definition within a Template (blueprint - not deployed)"""
    template = models.ForeignKey(
        Template,
        on_delete=models.CASCADE,
        related_name='services'
    )
    service_id = models.CharField(
        max_length=255,
        help_text="Service identifier (e.g., service_1)"
    )
    name = models.CharField(
        max_length=255,
        default='New Service',
        help_text="Service name"
    )
    image = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Docker image or source"
    )
    # Docker registry credentials
    registry_username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Docker registry username"
    )
    registry_password = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Docker registry password (encrypted)"
    )
    cpu = models.IntegerField(
        default=8,
        help_text="CPU allocation"
    )
    memory = models.IntegerField(
        default=8,
        help_text="Memory in GB"
    )
    variables = models.JSONField(
        default=dict,
        help_text="Environment variables"
    )
    networking = models.JSONField(
        default=dict,
        help_text="Networking configuration"
    )
    position_x = models.FloatField(
        default=0,
        help_text="X position on canvas"
    )
    position_y = models.FloatField(
        default=0,
        help_text="Y position on canvas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Template Service"
        verbose_name_plural = "Template Services"
        unique_together = ['template', 'service_id']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.name} ({self.template.name})"


# =============================================================================
# PROJECT - Actual Deployment on Railway
# =============================================================================

class Project(models.Model):
    """Actual deployment on Railway - created from Template or directly"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('deploying', 'Deploying'),
        ('deployed', 'Deployed'),
        ('failed', 'Failed'),
        ('stopped', 'Stopped'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    source_template = models.ForeignKey(
        Template,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deployed_projects',
        help_text="Template this project was created from (if any)"
    )
    name = models.CharField(
        max_length=255,
        help_text="Project name"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Project description"
    )
    # Railway identifiers
    railway_project_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Project ID"
    )
    railway_environment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Environment ID"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        help_text="Deployment status"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this project is active"
    )
    deployed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the project was deployed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"
    
    @property
    def services_count(self):
        return self.services.count()


class ProjectService(models.Model):
    """Actual deployed service on Railway"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('building', 'Building'),
        ('deploying', 'Deploying'),
        ('running', 'Running'),
        ('failed', 'Failed'),
        ('stopped', 'Stopped'),
    ]
    
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='services'
    )
    source_service = models.ForeignKey(
        TemplateService,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deployed_services',
        help_text="Template service this was created from (if any)"
    )
    service_id = models.CharField(
        max_length=255,
        help_text="Service identifier (e.g., service_1)"
    )
    name = models.CharField(
        max_length=255,
        default='New Service',
        help_text="Service name"
    )
    # Railway identifiers
    railway_service_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Service ID"
    )
    railway_deployment_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Railway Deployment ID"
    )
    # Service configuration
    image = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Docker image or source"
    )
    registry_username = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Docker registry username"
    )
    registry_password = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Docker registry password (encrypted)"
    )
    cpu = models.IntegerField(
        default=8,
        help_text="CPU allocation"
    )
    memory = models.IntegerField(
        default=8,
        help_text="Memory in GB"
    )
    variables = models.JSONField(
        default=dict,
        help_text="Environment variables"
    )
    networking = models.JSONField(
        default=dict,
        help_text="Networking configuration"
    )
    # Deployment info
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Service status"
    )
    public_url = models.URLField(
        blank=True,
        null=True,
        help_text="Public URL if networking is enabled"
    )
    # Canvas position
    position_x = models.FloatField(
        default=0,
        help_text="X position on canvas"
    )
    position_y = models.FloatField(
        default=0,
        help_text="Y position on canvas"
    )
    deployed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the service was deployed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Project Service"
        verbose_name_plural = "Project Services"
        unique_together = ['project', 'service_id']
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.name} ({self.project.name})"


# =============================================================================
# BACKWARD COMPATIBILITY - Alias for existing code
# =============================================================================

# Alias Service to TemplateService for backward compatibility
Service = TemplateService
