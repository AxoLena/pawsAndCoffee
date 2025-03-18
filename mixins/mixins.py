import requests
from rest_framework import status
from rest_framework.response import Response


class RequestsGETMixin:
    def get_dict(self, url, headers=None):
        url = url
        response = requests.get(url, headers=headers)
        dict = response.json()
        return dict


class GetAuthToken:
    def get_auth_token(self, request):
        try:
            token = request.COOKIES.get('auth-token')
            return {'Authorization': f'Token {token}'}
        except Exception:
            return Response(data='Токен не найден', status=status.HTTP_400_BAD_REQUEST)
