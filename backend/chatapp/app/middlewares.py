from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

class UserMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):

        try:
            user = JWTAuthentication().authenticate(request)
        except InvalidToken:
            user = None

        if user is not None:
            request.user_id = user[1]['user_id']
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        response = self.get_response(request, *args, **kwargs)
        return response
    

