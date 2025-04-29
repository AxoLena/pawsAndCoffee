from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseBadRequest

from Cats.models import FormForGuardianship
from Booking.models import Booking


@shared_task()
def send_order_notification(order_id, flag):
    match flag:
        case 'guardian':
            order = FormForGuardianship.objects.get(id=order_id)
            message = (f'Вы оформили опекунство на {order.cat_name}, '
                       f'ваш ежемесячный платеж составит {order.amount_of_money} рублей. '
                       f'Вы можете отменить подписку в любой момент в личном кабинете на нашем сайте или позвонив нам!')
        case 'booking':
            order = Booking.objects.get(id=order_id)
            message = (f'Вы купили билет в кото-кафе на сумму {order.cost}.'
                       f' Ждем вас {order.date} числа в {order.time} по адрессу {order.address}, не забудьте взять с собой хорошее настроение!')
        case _:
            return HttpResponseBadRequest(status=400)
    subject = f'Оплата покупки на сайте Paws&Coffe'
    receipent_email = order.email
    mail_to_sender = send_mail(subject=subject, message=message, from_email=settings.EMAIL_HOST_USER, receipent_email=[receipent_email],)
    return mail_to_sender
