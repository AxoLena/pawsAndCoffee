from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

from Users.models import CustomUser




def auth_token(get_response):
    def middleware(request):
        response = get_response(request)
        token = request.COOKIES.get('auth-token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            url = reverse('users:logout_delToken')
            if request.path != url:
                try:
                    request.user = CustomUser.objects.get(auth_token=token)
                except ObjectDoesNotExist:
                    response.delete_cookie('auth-token')
                    request.user = AnonymousUser()
        else:
            request.user = AnonymousUser()
        return response
    return middleware
