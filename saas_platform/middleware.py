"""
Custom middleware for HTMX support
"""
from django.utils.deprecation import MiddlewareMixin


class HtmxMiddleware(MiddlewareMixin):
    """
    Middleware to add HTMX-related context to requests
    """
    def process_request(self, request):
        request.htmx = request.headers.get('HX-Request', False)
        request.htmx_boosted = request.headers.get('HX-Boosted', False)
        request.htmx_current_url = request.headers.get('HX-Current-URL', '')
        request.htmx_history_restore_request = request.headers.get('HX-History-Restore-Request', False)
        request.htmx_prompt = request.headers.get('HX-Prompt', '')
        request.htmx_target = request.headers.get('HX-Target', '')
        request.htmx_trigger = request.headers.get('HX-Trigger', '')
        request.htmx_trigger_name = request.headers.get('HX-Trigger-Name', '')

