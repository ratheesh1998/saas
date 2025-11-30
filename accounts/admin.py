from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import (
    User, RailwaySettings, 
    Template, TemplateService,
    Project, ProjectService
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email', 'username')
    ordering = ('-date_joined',)


@admin.register(RailwaySettings)
class RailwaySettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'railway_workspace_id', 'has_token', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'railway_workspace_id')
    readonly_fields = ('created_at', 'updated_at')
    
    def has_token(self, obj):
        return bool(obj.railway_token)
    has_token.boolean = True
    has_token.short_description = 'Token Set'
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Railway Credentials', {
            'fields': ('railway_template_id', 'railway_workspace_id', 'railway_token')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# TEMPLATE ADMIN
# =============================================================================

class TemplateServiceInline(admin.TabularInline):
    model = TemplateService
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('service_id', 'name', 'image', 'cpu', 'memory', 'position_x', 'position_y')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'services_count', 'is_published', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_published', 'created_at', 'user')
    search_fields = ('name', 'user__email', 'description')
    readonly_fields = ('created_at', 'updated_at', 'services_count')
    raw_id_fields = ('user',)
    inlines = [TemplateServiceInline]
    
    actions = ['publish_templates']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'is_published')
        }),
        ('Configuration', {
            'fields': ('template_config',),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('services_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = 'Services'
    
    def publish_templates(self, request, queryset):
        for template in queryset:
            if not template.is_published:
                template.publish()
        self.message_user(request, f"{queryset.count()} template(s) published successfully.")
    publish_templates.short_description = "Publish selected templates"


@admin.register(TemplateService)
class TemplateServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_id', 'template', 'image', 'cpu', 'memory', 'created_at')
    list_filter = ('created_at', 'template__user')
    search_fields = ('name', 'service_id', 'image', 'template__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('template',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('template', 'service_id', 'name')
        }),
        ('Source', {
            'fields': ('image', 'registry_username', 'registry_password')
        }),
        ('Resources', {
            'fields': ('cpu', 'memory')
        }),
        ('Configuration', {
            'fields': ('variables', 'networking'),
            'classes': ('collapse',)
        }),
        ('Canvas Position', {
            'fields': ('position_x', 'position_y'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# =============================================================================
# PROJECT ADMIN
# =============================================================================

class ProjectServiceInline(admin.TabularInline):
    model = ProjectService
    extra = 0
    readonly_fields = ('created_at', 'updated_at', 'railway_service_id', 'status', 'public_url')
    fields = ('service_id', 'name', 'image', 'status', 'railway_service_id', 'public_url')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'source_template', 'status_badge', 'services_count', 'railway_project_id', 'deployed_at')
    list_filter = ('status', 'is_active', 'created_at', 'user')
    search_fields = ('name', 'user__email', 'railway_project_id', 'description')
    readonly_fields = ('created_at', 'updated_at', 'services_count', 'deployed_at')
    raw_id_fields = ('user', 'source_template')
    inlines = [ProjectServiceInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'source_template')
        }),
        ('Status', {
            'fields': ('status', 'is_active', 'deployed_at')
        }),
        ('Railway IDs', {
            'fields': ('railway_project_id', 'railway_environment_id'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('services_count',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def services_count(self, obj):
        return obj.services.count()
    services_count.short_description = 'Services'
    
    def status_badge(self, obj):
        colors = {
            'draft': '#6b7280',
            'deploying': '#f59e0b',
            'deployed': '#10b981',
            'failed': '#ef4444',
            'stopped': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(ProjectService)
class ProjectServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_id', 'project', 'status_badge', 'image', 'railway_service_id', 'public_url_link')
    list_filter = ('status', 'created_at', 'project__user')
    search_fields = ('name', 'service_id', 'image', 'project__name', 'railway_service_id')
    readonly_fields = ('created_at', 'updated_at', 'deployed_at')
    raw_id_fields = ('project', 'source_service')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('project', 'source_service', 'service_id', 'name')
        }),
        ('Railway IDs', {
            'fields': ('railway_service_id', 'railway_deployment_id')
        }),
        ('Status', {
            'fields': ('status', 'public_url', 'deployed_at')
        }),
        ('Source', {
            'fields': ('image', 'registry_username', 'registry_password')
        }),
        ('Resources', {
            'fields': ('cpu', 'memory')
        }),
        ('Configuration', {
            'fields': ('variables', 'networking'),
            'classes': ('collapse',)
        }),
        ('Canvas Position', {
            'fields': ('position_x', 'position_y'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#6b7280',
            'building': '#3b82f6',
            'deploying': '#f59e0b',
            'running': '#10b981',
            'failed': '#ef4444',
            'stopped': '#6b7280',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 11px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def public_url_link(self, obj):
        if obj.public_url:
            return format_html('<a href="{}" target="_blank">{}</a>', obj.public_url, obj.public_url[:30] + '...')
        return '-'
    public_url_link.short_description = 'Public URL'
