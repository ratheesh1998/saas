from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, RailwaySettingsForm, TemplateCreationForm
from .models import RailwaySettings, Template, Service
import random
import json

def register_view(request):
    """Handle user registration with HTMX"""
    if request.user.is_authenticated:
        if hasattr(request, 'htmx') and request.htmx:
            dashboard_url = reverse('core:dashboard')
            return HttpResponse(
                f'<script>window.location.href = "{dashboard_url}";</script>'
            )
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if hasattr(request, 'htmx') and request.htmx:
                return HttpResponse(
                    render_to_string('accounts/partials/register_success.html', 
                                   {'user': user}, request=request)
                )
            messages.success(request, 'Registration successful!')
            return redirect('core:dashboard')
        else:
            if hasattr(request, 'htmx') and request.htmx:
                return HttpResponse(
                    render_to_string('accounts/partials/register_form.html', 
                                   {'form': form}, request=request)
                )
    else:
        form = CustomUserCreationForm()
    
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('accounts/partials/register_form.html', 
                           {'form': form}, request=request)
        )
    
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Handle user login with HTMX"""
    if request.user.is_authenticated:
        if hasattr(request, 'htmx') and request.htmx:
            dashboard_url = reverse('core:dashboard')
            return HttpResponse(
                f'<script>window.location.href = "{dashboard_url}";</script>'
            )
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if hasattr(request, 'htmx') and request.htmx:
                    return HttpResponse(
                        render_to_string('accounts/partials/login_success.html', 
                                       {'user': user}, request=request)
                    )
                messages.success(request, f'Welcome back, {user.email}!')
                return redirect('core:dashboard')
        else:
            if hasattr(request, 'htmx') and request.htmx:
                return HttpResponse(
                    render_to_string('accounts/partials/login_form.html', 
                                   {'form': form}, request=request)
                )
    else:
        form = CustomAuthenticationForm()
    
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('accounts/partials/login_form.html', 
                           {'form': form}, request=request)
        )
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def profile_view(request):
    """User profile view"""
    context = {'user': request.user}
    
    # If HTMX request, return only the content partial
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('accounts/partials/profile_content.html', context, request=request)
        )
    
    # Full page render
    return render(request, 'accounts/profile.html', context)


# Breaking Bad character names for random template naming
BREAKING_BAD_NAMES = [
    "Heisenberg", "Skyler", "Jesse", "Saul", "Gus", "Hank", "Marie",
    "Walter Jr", "Tuco", "Mike", "Badger", "Skinny Pete", "Combo",
    "Jane", "Andrea", "Brock", "Todd", "Lydia", "Huell", "Kuby",
    "Gale", "Victor", "Tyrus", "Leonel", "Marco", "Don Eladio",
    "Hector", "Tortuga", "Gonzo", "No-Doze", "Spooge", "Wendy",
    "Old Joe", "Emilio", "Krazy-8", "Domingo", "Jimmy", "Kim",
    "Chuck", "Howard", "Lalo", "Nacho", "Francesca", "Erin"
]

def generate_breaking_bad_template_name(user):
    """Generate a unique Breaking Bad-inspired template name for a user"""
    # Get all existing template names for this user
    existing_names = set(
        Template.objects.filter(user=user, is_active=True).values_list('name', flat=True)
    )
    
    # Try to find an unused name
    available_names = [name for name in BREAKING_BAD_NAMES if name not in existing_names]
    
    if available_names:
        return random.choice(available_names)
    
    # If all names are used, append a number
    base_name = random.choice(BREAKING_BAD_NAMES)
    counter = 1
    while f"{base_name} {counter}" in existing_names:
        counter += 1
    return f"{base_name} {counter}"


@login_required
def quick_create_template(request):
    """Quickly create a new template with a random Breaking Bad-inspired name"""
    # Generate a random Breaking Bad name
    template_name = generate_breaking_bad_template_name(request.user)
    
    # Create the template with minimal configuration
    template = Template.objects.create(
        user=request.user,
        name=template_name,
        description=f"Template created on {request.user.email}",
        template_config={"input": {"serializedConfig": {"services": {}}, "workspaceId": None, "templateId": None, "environmentId": None, "projectId": None}}
    )
    
    # For HTMX requests, return the template editor directly
    if hasattr(request, 'htmx') and request.htmx:
        # Set up context for template editor
        context = {
            'template_action': 'create',
            'template_id': template.id,
            'active_tab': 'template',
            'template_name': template.name,
        }
        
        # Create response with template editor content
        response = HttpResponse(
            render_to_string('accounts/partials/template_editor.html', context, request=request)
        )
        
        # Push the new URL to browser history so reload works
        response['HX-Push-Url'] = f'{reverse("accounts:settings")}?tab=template&action=create&template_id={template.id}'
        
        return response
    
    # For regular requests (fallback)
    messages.success(request, f'Template "{template.name}" created successfully!')
    return redirect(f'{reverse("accounts:settings")}?tab=template&action=create&template_id={template.id}')


@login_required
@require_http_methods(["POST"])
def create_service(request):
    """Create a new service for a template"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        service_id = data.get('service_id')
        
        # Get the template
        template = get_object_or_404(Template, id=template_id, user=request.user)
        
        # Check if service already exists
        service, created = Service.objects.get_or_create(
            template=template,
            service_id=service_id,
            defaults={
                'name': data.get('name', 'New Service'),
                'image': data.get('image', ''),
                'cpu': data.get('cpu', 8),
                'memory': data.get('memory', 8),
                'variables': data.get('variables', {}),
                'networking': data.get('networking', {'http': False, 'tcp': False}),
                'position_x': data.get('position', {}).get('x', 0),
                'position_y': data.get('position', {}).get('y', 0),
            }
        )
        
        return JsonResponse({
            'success': True,
            'service_id': service.service_id,
            'id': service.id,
            'created': created,
            'message': 'Service created successfully' if created else 'Service already exists'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def update_service(request):
    """Update an existing service"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        service_id = data.get('service_id')
        
        # Get the template and service
        template = get_object_or_404(Template, id=template_id, user=request.user)
        service = get_object_or_404(Service, template=template, service_id=service_id)
        
        # Update service fields
        if 'name' in data:
            service.name = data['name']
        if 'image' in data:
            service.image = data['image']
        if 'cpu' in data:
            service.cpu = data['cpu']
        if 'memory' in data:
            service.memory = data['memory']
        if 'variables' in data:
            service.variables = data['variables']
        if 'networking' in data:
            service.networking = data['networking']
        if 'position' in data:
            service.position_x = data['position'].get('x', service.position_x)
            service.position_y = data['position'].get('y', service.position_y)
        if 'registry_username' in data:
            service.registry_username = data['registry_username']
        if 'registry_password' in data:
            service.registry_password = data['registry_password']
        
        service.save()
        
        return JsonResponse({
            'success': True,
            'service_id': service.service_id,
            'message': 'Service updated successfully'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["POST"])
def validate_docker_image(request):
    """Validate if a Docker image exists on Docker Hub"""
    try:
        data = json.loads(request.body)
        image_name = data.get('image', '').strip()
        
        if not image_name:
            return JsonResponse({
                'success': False,
                'error': 'No image name provided'
            }, status=400)
        
        # Parse image name (handle formats like: image:tag, user/image:tag, registry.com/user/image:tag)
        import requests
        
        # Extract repository and tag
        if ':' in image_name:
            repository, tag = image_name.rsplit(':', 1)
        else:
            repository = image_name
            tag = 'latest'
        
        # Check if it's a Docker Hub image (no registry prefix)
        if '/' not in repository or repository.count('/') == 1:
            # This is a Docker Hub image
            # Format: library/image or username/image
            if '/' not in repository:
                repository = f'library/{repository}'
            
            # Check Docker Hub API
            api_url = f'https://hub.docker.com/v2/repositories/{repository}/tags/{tag}'
            
            try:
                response = requests.get(api_url, timeout=5)
                
                if response.status_code == 200:
                    return JsonResponse({
                        'success': True,
                        'exists': True,
                        'message': 'Image found on Docker Hub'
                    })
                elif response.status_code == 404:
                    return JsonResponse({
                        'success': True,
                        'exists': False,
                        'message': 'Image not found on Docker Hub'
                    })
                else:
                    return JsonResponse({
                        'success': True,
                        'exists': False,
                        'message': 'Unable to verify image'
                    })
            except requests.RequestException:
                return JsonResponse({
                    'success': True,
                    'exists': False,
                    'message': 'Unable to verify image - timeout or network error'
                })
        else:
            # This is from another registry (gcr.io, ghcr.io, etc.)
            return JsonResponse({
                'success': True,
                'exists': False,
                'message': 'Cannot verify images from custom registries'
            })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@require_http_methods(["GET"])
def get_services(request, template_id):
    """Get all services for a template"""
    try:
        # Get the template
        template = get_object_or_404(Template, id=template_id, user=request.user)
        
        # Get all services for this template
        services = Service.objects.filter(template=template)
        
        # Serialize services
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
                'position': {
                    'x': service.position_x,
                    'y': service.position_y
                },
                'has_credentials': bool(service.registry_username and service.registry_password),
                'registry_username': service.registry_username or ''
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
def view_template(request, template_id):
    """View/Edit an existing template"""
    template = get_object_or_404(Template, id=template_id, user=request.user, is_active=True)
    
    # Get user's railway settings
    railway_settings, _ = RailwaySettings.objects.get_or_create(user=request.user)
    
    context = {
        'template_action': 'create',  # Using 'create' action to show editor
        'template_id': template.id,
        'active_tab': 'template',
        'template_name': template.name,
        'template_description': template.description or '',
        'settings': railway_settings,
    }
    
    # For HTMX requests, return the template editor
    if hasattr(request, 'htmx') and request.htmx:
        response = HttpResponse(
            render_to_string('accounts/partials/template_editor.html', context, request=request)
        )
        # Push URL to browser history
        response['HX-Push-Url'] = f'{reverse("accounts:settings")}?tab=template&action=create&template_id={template.id}'
        return response
    
    # For regular requests, redirect to settings with template editor
    return redirect(f'{reverse("accounts:settings")}?tab=template&action=create&template_id={template.id}')


@login_required
@require_http_methods(["POST", "DELETE"])
def delete_template(request, template_id):
    """Delete a template (soft delete by setting is_active=False)"""
    template = get_object_or_404(Template, id=template_id, user=request.user)
    
    template_name = template.name
    
    # Soft delete - set is_active to False
    template.is_active = False
    template.save()
    
    # Delete associated services (hard delete since template is soft-deleted)
    Service.objects.filter(template=template).delete()
    
    messages.success(request, f'Template "{template_name}" deleted successfully!')
    
    # Get updated templates list for response
    user_templates = Template.objects.filter(user=request.user, is_active=True)
    
    context = {
        'templates': user_templates,
        'active_tab': 'template',
        'template_action': None,
    }
    
    # For HTMX requests, return the updated template list
    if hasattr(request, 'htmx') and request.htmx:
        response = HttpResponse(
            render_to_string('accounts/partials/settings_tab_content.html', context, request=request)
        )
        # Push URL to remove template_id from URL
        response['HX-Push-Url'] = f'{reverse("accounts:settings")}?tab=template'
        return response
    
    return redirect(f'{reverse("accounts:settings")}?tab=template')


@login_required
def settings_view(request):
    """Railway settings view with HTMX support and tabs"""
    # Get or create RailwaySettings for the user
    railway_settings, created = RailwaySettings.objects.get_or_create(
        user=request.user
    )
    
    # Get active tab from request (default to 'config')
    active_tab = request.GET.get('tab', 'config')
    if active_tab not in ['config', 'template']:
        active_tab = 'config'
    
    # Get action for templates (create, view, etc.)
    template_action = request.GET.get('action', None)
    
    # Get user's templates
    user_templates = Template.objects.filter(user=request.user, is_active=True)
    
    context = {
        'settings': railway_settings,
        'active_tab': active_tab,
        'templates': user_templates,
        'template_action': template_action,
    }
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type', 'config')
        
        if form_type == 'config':
            # Handle Railway Settings form
            form = RailwaySettingsForm(request.POST, instance=railway_settings)
            context['settings_form'] = form
            context['active_tab'] = 'config'  # Ensure we stay on config tab
            if form.is_valid():
                form.save()
                # Refresh the instance to get updated data
                railway_settings.refresh_from_db()
                # Re-initialize form with saved data to preserve input values
                form = RailwaySettingsForm(instance=railway_settings)
                context['settings_form'] = form
                messages.success(request, 'Railway settings saved successfully!')
                
                # If HTMX request, return the form with success message
                if hasattr(request, 'htmx') and request.htmx:
                    if hasattr(request, 'htmx_target') and request.htmx_target == 'settings-form-container':
                        return HttpResponse(
                            render_to_string('accounts/partials/settings_form.html', 
                                           context, 
                                           request=request)
                        )
                    return HttpResponse(
                        render_to_string('accounts/partials/settings_tab_content.html', 
                                       context, 
                                       request=request)
                    )
                return redirect('accounts:settings?tab=config')
            else:
                # Form has errors
                if hasattr(request, 'htmx') and request.htmx:
                    if hasattr(request, 'htmx_target') and request.htmx_target == 'settings-form-container':
                        return HttpResponse(
                            render_to_string('accounts/partials/settings_form.html', 
                                           context, 
                                           request=request)
                        )
                    return HttpResponse(
                        render_to_string('accounts/partials/settings_tab_content.html', 
                                       context, 
                                       request=request)
                    )
        
        elif form_type == 'template':
            # Handle Template Creation form
            # Get template_config from POST data (sent as JSON string)
            template_config_str = request.POST.get('template_config', '{}')
            import json
            try:
                # Parse the JSON to validate it
                template_config = json.loads(template_config_str)
                # Create a mutable copy of POST data and convert to JSON string for form
                post_data = request.POST.copy()
                # The form expects template_config as a JSON string
                template_form = TemplateCreationForm({
                    'name': request.POST.get('name', ''),
                    'description': request.POST.get('description', ''),
                    'template_config': template_config_str
                }, user=request.user)
            except json.JSONDecodeError as e:
                # If JSON is invalid, create form with error
                template_form = TemplateCreationForm(request.POST, user=request.user)
                template_form.add_error('template_config', f'Invalid JSON: {str(e)}')
            except Exception as e:
                template_form = TemplateCreationForm(request.POST, user=request.user)
            
            context['template_form'] = template_form
            context['active_tab'] = 'template'  # Ensure we stay on template tab
            if template_form.is_valid():
                template = template_form.save()
                messages.success(request, f'Template "{template.name}" created successfully!')
                context['templates'] = Template.objects.filter(user=request.user, is_active=True)
                # Reset form after successful submission
                context['template_form'] = TemplateCreationForm(user=request.user)
                
                # If HTMX request, return the form with success message
                if hasattr(request, 'htmx') and request.htmx:
                    if hasattr(request, 'htmx_target') and request.htmx_target == 'template-form-container':
                        return HttpResponse(
                            render_to_string('accounts/partials/template_form.html', 
                                           context, 
                                           request=request)
                        )
                    # Return template tab content to refresh template list
                    return HttpResponse(
                        render_to_string('accounts/partials/settings_tab_content.html', 
                                       context, 
                                       request=request)
                    )
                return redirect('accounts:settings?tab=template')
            else:
                # Form has errors
                if hasattr(request, 'htmx') and request.htmx:
                    if hasattr(request, 'htmx_target') and request.htmx_target == 'template-form-container':
                        return HttpResponse(
                            render_to_string('accounts/partials/template_form.html', 
                                           context, 
                                           request=request)
                        )
                    return HttpResponse(
                        render_to_string('accounts/partials/settings_tab_content.html', 
                                       context, 
                                       request=request)
                    )
    else:
        # GET request - initialize forms
        if 'settings_form' not in context:
            context['settings_form'] = RailwaySettingsForm(instance=railway_settings)
        if 'template_form' not in context:
            context['template_form'] = TemplateCreationForm(user=request.user)
    
    # If HTMX request, check what to return
    if hasattr(request, 'htmx') and request.htmx:
        # If target is settings-main-content, return only tab content
        if hasattr(request, 'htmx_target') and request.htmx_target == 'settings-main-content':
            return HttpResponse(
                render_to_string('accounts/partials/settings_tab_content.html', 
                               context, 
                               request=request)
            )
        # If target is template-content, return template content
        if hasattr(request, 'htmx_target') and request.htmx_target == 'template-content':
            return HttpResponse(
                render_to_string('accounts/partials/settings_tab_content.html', 
                               context, 
                               request=request)
            )
        # Otherwise return full settings content
        return HttpResponse(
            render_to_string('accounts/partials/settings_content.html', 
                           context, 
                           request=request)
        )
    
    # Full page render
    return render(request, 'accounts/settings.html', context)

