from django.shortcuts import render
class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            return render(request, 'polls/404.html', {'path': request.path})

        if response.status_code == 500:
            return render(request, 'polls/500.html')

        return response