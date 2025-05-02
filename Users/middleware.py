from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from Users.models import CustomUser


class AuthTokenMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def process_request(self, request):
        token = request.COOKIES.get('auth-token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            url = reverse('users:logout_delToken')
            if request.path != url:
                try:
                    request.user = CustomUser.objects.get(auth_token=token)
                    request.delete_cookie = False
                except ObjectDoesNotExist:
                    request.user = AnonymousUser()
                    request.delete_cookie = True
        else:
            request.user = AnonymousUser()
            request.delete_cookie = False
        return None

    def process_response(self, request, response):
        if request.delete_cookie:
            response.delete_cookie('auth-token')
        return response

