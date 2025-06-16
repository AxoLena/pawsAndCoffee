from django.core.cache import cache
from django.test import Client
from rest_framework import status
from rest_framework.response import Response


class GetAuthTokenMixin:
    def get_auth_token(self, request):
        try:
            token = request.COOKIES.get('auth-token')
            return {'Authorization': f'Token {token}'}
        except Exception:
            return Response(data='Токен не найден', status=status.HTTP_400_BAD_REQUEST)


class GetCacheMixin:
    def get_cache_for_context(self, cache_name, url, time, headers=None, request = None):
        if request:
            print(request.user)
        cache_list = cache.get(cache_name)
        if cache_list:
            return cache_list
        else:
            client = Client()
            url = url
            response = client.get(url, headers, request)
            data = response.json()
            cache.set(cache_name, data, time)
            return data
