from celery import shared_task
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from djoser import utils


@shared_task()
def custom_reset_password(user, request):
    token = default_token_generator.make_token(user)
    uid = utils.encode_uid(user.pk)
    reset_password_url = request.build_absolute_uri(reverse('users:new_password'))
    context = {
        'url': reset_password_url,
        'uid': uid,
        'token': token
    }
    return context
