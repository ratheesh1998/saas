from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from accounts.models import Project, ProjectService, Template, RailwaySettings
import random

# Breaking Bad character names for random project naming
BREAKING_BAD_NAMES = [
    "Heisenberg", "Skyler", "Jesse", "Saul", "Gus", "Hank", "Marie",
    "Walter Jr", "Tuco", "Mike", "Badger", "Skinny Pete", "Combo",
    "Jane", "Andrea", "Brock", "Todd", "Lydia", "Huell", "Kuby",
    "Gale", "Victor", "Tyrus", "Leonel", "Marco", "Don Eladio",
    "Hector", "Tortuga", "Gonzo", "No-Doze", "Spooge", "Wendy",
    "Old Joe", "Emilio", "Krazy-8", "Domingo", "Jimmy", "Kim",
    "Chuck", "Howard", "Lalo", "Nacho", "Francesca", "Erin"
]


def generate_project_name(user):
    """Generate a unique Breaking Bad-inspired project name for a user"""
    existing_names = set(
        Project.objects.filter(user=user, is_active=True).values_list('name', flat=True)
    )
    
    available_names = [name for name in BREAKING_BAD_NAMES if name not in existing_names]
    
    if available_names:
        return random.choice(available_names)
    
    base_name = random.choice(BREAKING_BAD_NAMES)
    counter = 1
    while f"{base_name} {counter}" in existing_names:
        counter += 1
    return f"{base_name} {counter}"


def home_view(request):
    """Home page view"""
    return render(request, 'core/home.html')


@login_required
def dashboard_view(request):
    """Dashboard view - shows user's Projects (actual deployments)"""
    # Get user's projects (actual deployments)
    projects = Project.objects.filter(user=request.user, is_active=True)
    
    context = {
        'user': request.user,
        'projects': projects,
    }
    
    # If HTMX request, return only the content partial
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('core/partials/dashboard_content.html', context, request=request)
        )
    
    # Full page render
    return render(request, 'core/dashboard.html', context)


@login_required
def create_project(request):
    """Create a new empty project and show the grid editor"""
    # Generate a random project name
    project_name = generate_project_name(request.user)
    
    # Create the Project (actual deployment entity)
    project = Project.objects.create(
        user=request.user,
        name=project_name,
        description=f"Project created by {request.user.email}",
        status='draft'
    )
    
    # Get railway settings for the editor
    railway_settings, _ = RailwaySettings.objects.get_or_create(user=request.user)
    
    context = {
        'project': project,
        'project_id': project.id,
        'project_name': project.name,
        'project_description': project.description or '',
        'settings': railway_settings,
        'is_project': True,  # Flag to indicate this is a Project, not Template
    }
    
    # For HTMX requests, return the project editor
    if hasattr(request, 'htmx') and request.htmx:
        response = HttpResponse(
            render_to_string('core/partials/project_editor.html', context, request=request)
        )
        # Push URL to browser history
        response['HX-Push-Url'] = f'{reverse("core:project_view", args=[project.id])}'
        return response
    
    # For regular requests, redirect to project view
    return redirect('core:project_view', project_id=project.id)


@login_required
def project_view(request, project_id):
    """View/Edit a project"""
    project = get_object_or_404(Project, id=project_id, user=request.user, is_active=True)
    railway_settings, _ = RailwaySettings.objects.get_or_create(user=request.user)
    
    context = {
        'project': project,
        'project_id': project.id,
        'project_name': project.name,
        'project_description': project.description or '',
        'settings': railway_settings,
        'is_project': True,
    }
    
    # For HTMX requests, return just the editor
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('core/partials/project_editor.html', context, request=request)
        )
    
    # Full page render
    return render(request, 'core/project.html', context)


# =============================================================================
# PROJECT SERVICE API ENDPOINTS
# =============================================================================

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json


@login_required
@require_http_methods(["POST"])
def create_project_service(request):
    """Create or update a service in a project"""
    try:
        data = json.loads(request.body)
        project_id = data.get('project_id')
        service_id = data.get('service_id')
        
        # Get the project
        project = get_object_or_404(Project, id=project_id, user=request.user)
        
        # Create or update service
        service, created = ProjectService.objects.update_or_create(
            project=project,
            service_id=service_id,
            defaults={
                'name': data.get('name', 'New Service'),
                'image': data.get('image', ''),
                'cpu': data.get('cpu', 8),
                'memory': data.get('memory', 8),
                'variables': data.get('variables', {}),
                'networking': data.get('networking', {}),
                'position_x': data.get('position', {}).get('x', 0),
                'position_y': data.get('position', {}).get('y', 0),
            }
        )
        
        return JsonResponse({
            'success': True,
            'service_id': service.service_id,
            'id': service.id,
            'created': created,
            'message': 'Service created' if created else 'Service updated'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["GET"])
def get_project_services(request, project_id):
    """Get all services for a project"""
    try:
        project = get_object_or_404(Project, id=project_id, user=request.user)
        services = ProjectService.objects.filter(project=project)
        
        services_data = []
        for service in services:
            services_data.append({
                'id': service.id,
                'service_id': service.service_id,
                'name': service.name,
                'image': service.image or '',
                'cpu': service.cpu,
                'memory': service.memory,
                'variables': service.variables,
                'networking': service.networking,
                'status': service.status,
                'position': {
                    'x': service.position_x,
                    'y': service.position_y
                }
            })
        
        return JsonResponse({
            'success': True,
            'services': services_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def delete_project_service(request, project_id, service_id):
    """Delete a service from a project"""
    try:
        project = get_object_or_404(Project, id=project_id, user=request.user)
        service = get_object_or_404(ProjectService, project=project, service_id=service_id)
        
        service.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Service deleted'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

