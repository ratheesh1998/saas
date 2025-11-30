from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from accounts.models import Template, RailwaySettings
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
        Template.objects.filter(user=user, is_active=True).values_list('name', flat=True)
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
    """Dashboard view for authenticated users"""
    # Get user's templates/projects
    projects = Template.objects.filter(user=request.user, is_active=True)
    
    # Add service count to each project
    projects_with_counts = []
    for project in projects:
        project.services_count = project.services.count()
        projects_with_counts.append(project)
    
    context = {
        'user': request.user,
        'projects': projects_with_counts,
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
    
    # Create the project/template
    project = Template.objects.create(
        user=request.user,
        name=project_name,
        description=f"Project created by {request.user.email}",
        template_config={"input": {"serializedConfig": {"services": {}}, "workspaceId": None, "templateId": None, "environmentId": None, "projectId": None}}
    )
    
    # Get railway settings for the editor
    railway_settings, _ = RailwaySettings.objects.get_or_create(user=request.user)
    
    context = {
        'template_action': 'create',
        'template_id': project.id,
        'template_name': project.name,
        'template_description': project.description or '',
        'settings': railway_settings,
        'active_tab': 'template',
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
    from django.shortcuts import get_object_or_404
    
    project = get_object_or_404(Template, id=project_id, user=request.user, is_active=True)
    railway_settings, _ = RailwaySettings.objects.get_or_create(user=request.user)
    
    context = {
        'template_action': 'create',
        'template_id': project.id,
        'template_name': project.name,
        'template_description': project.description or '',
        'settings': railway_settings,
        'active_tab': 'template',
    }
    
    # For HTMX requests, return just the editor
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('core/partials/project_editor.html', context, request=request)
        )
    
    # Full page render
    return render(request, 'core/project.html', context)

