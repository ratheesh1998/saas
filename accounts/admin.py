from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, RailwaySettings, Template

admin.site.register(User, UserAdmin)


@admin.register(RailwaySettings)
class RailwaySettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'railway_template_id', 'railway_workspace_id', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email', 'railway_template_id', 'railway_workspace_id')
    readonly_fields = ('created_at', 'updated_at')
    
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


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'railway_template_id', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('name', 'user__email', 'railway_template_id', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'name', 'description', 'is_active')
        }),
        ('Railway Configuration', {
            'fields': ('railway_template_id', 'template_config')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

