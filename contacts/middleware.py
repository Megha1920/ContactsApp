from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_urls = [
            '/login/',
            '/register/',
            '/landing_page/',
            '/admin/'
        ]
        
        logger.debug(f"Request path: {request.path}")
        logger.debug(f"Exempt URLs: {exempt_urls}")
        
        if not request.user.is_authenticated and request.path in exempt_urls:
            logger.debug("Request path is exempted. Proceeding without redirection.")
            response = self.get_response(request)
            return response
        
        if not request.user.is_authenticated:
            logger.debug("User is not authenticated. Redirecting to login.")
            return redirect('/login/')
        
        response = self.get_response(request)
        return response
