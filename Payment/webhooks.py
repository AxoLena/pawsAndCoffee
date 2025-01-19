import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from yookassa import Webhook, Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import WebhookNotificationFactory, WebhookNotificationEventType

from Booking.models import Booking, Schedule
from Cats.models import FormForGuardianship


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.mode == 'payment' and session.payment_status == 'paid':
            if session.extra_param == 'guardian':
                try:
                    guardian_id = session.client_reference_id
                except FormForGuardianship.DoesNotExist:
                    return HttpResponse(status=404)
                guardian = FormForGuardianship.objects.get(id=guardian_id)
                guardian.update(is_paid=True)
            else:
                try:
                    user_id = session.client_reference_id
                except Booking.DoesNotExist:
                    return HttpResponse(status=404)
                user = Booking.objects.get(id=user_id)
                user.update(is_paid=True)

                number_of_places = Schedule.objects.get(date=user['date'], time=user['time'])
                number_of_places.quantity -= user['quantity']
                number_of_places.save()

    return HttpResponse(status=200)


@csrf_exempt
def yookassa_webhook(request):
    ip = get_client_ip(request)
    if not SecurityHelper().is_ip_trusted(ip):
        return HttpResponse(status=400)

    event_json = json.loads(request.body)
    try:
        notification_object = WebhookNotificationFactory().create(event_json)
        response_object = notification_object.object
        if notification_object.event == WebhookNotificationEventType.PAYMENT_SUCCEEDED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }

        elif notification_object.event == WebhookNotificationEventType.PAYMENT_CANCELED:
            some_data = {
                'paymentId': response_object.id,
                'paymentStatus': response_object.status,
            }
        else:
            return HttpResponse(status=400)

        Configuration.configure(account_id=settings.YOOKASSA_SHOP_ID, secret_key=settings.YOOKASSA_SECRET_KEY)

        payment_info = Payment.find_one(some_data['paymentId'])
        if payment_info:
            payment_status = payment_info.status
        else:
            return HttpResponse(status=400)

    except Exception:
        return HttpResponse(status=400)

    return HttpResponse(200)