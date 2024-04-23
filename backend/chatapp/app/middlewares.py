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
            print(user)
        except InvalidToken:
            user = None

        if user is not None:
            # Nếu người dùng đã được xác thực, trả về ID của người dùng
            request.user_id = user[1]['user_id']
        else:
            return JsonResponse({'error': 'User is not authenticated'}, status=401)

        # Truyền thêm các đối số và từ khóa (args và kwargs) cho __call__
        response = self.get_response(request, *args, **kwargs)
        return response
    

