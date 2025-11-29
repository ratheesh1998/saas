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
from .models import RailwaySettings, Template

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

