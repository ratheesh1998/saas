from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import render_to_string

def home_view(request):
    """Home page view"""
    return render(request, 'core/home.html')

@login_required
def dashboard_view(request):
    """Dashboard view for authenticated users"""
    context = {'user': request.user}
    
    # If HTMX request, return only the content partial
    if hasattr(request, 'htmx') and request.htmx:
        return HttpResponse(
            render_to_string('core/partials/dashboard_content.html', context, request=request)
        )
    
    # Full page render
    return render(request, 'core/dashboard.html', context)

