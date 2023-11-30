from django.shortcuts import redirect
from django.urls import reverse

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the user is logged out and trying to access a restricted route
        if not request.user.is_authenticated and request.path in ['/restricted-route/', '/','post_new']:
            return redirect(reverse('login'))  # Redirect to the login page

        return response
