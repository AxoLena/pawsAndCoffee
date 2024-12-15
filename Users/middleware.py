from django.contrib.auth.models import AnonymousUser
from django.urls import reverse

from Users.models import User


def auth_token(get_response):
    def middleware(request):
        token = request.COOKIES.get('auth-token')
        if token:
            request.META['HTTP_AUTHORIZATION'] = f'Token {token}'
            url = reverse('users:logout_delToken')
            if request.path != url:
                request.user = User.objects.get(auth_token=token)
        else:
            request.user = AnonymousUser()
        return get_response(request)
    return middleware
