import json

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe
from yookassa import Configuration, Payment
from yookassa.domain.common import SecurityHelper
from yookassa.domain.notification import WebhookNotificationFactory, WebhookNotificationEventType

from Booking.models import Booking, Schedule
from Cats.models import FormForGuardianship
from Payment.models import CheckoutSessionStripe
from Payment.tasks import send_order_notification


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

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == 'paid':
            match session.mode:
                case'payment':
                    try:
                        booking_id = session.client_reference_id
                    except Booking.DoesNotExist:
                        return HttpResponse(status=404)
                    booking = Booking.objects.get(id=booking_id)
                    booking.is_paid = True
                    number_of_places = Schedule.objects.get(date=booking.date, time=booking.time)
                    number_of_places.quantity -= booking.quantity
                    number_of_places.save()
                    if booking.user and not booking.coupon and booking.bonuses != 0:
                        user = booking.user
                        user.coins.increased(discount=10, payment_amount=booking.cost,
                                             description=f'Бронь на {booking.data} {booking.time}')
                        user.save()
                    send_order_notification.delay(order_id=booking_id, flag='booking')
                    booking.save()

                case 'subscription':
                    try:
                        guardian_id = session.client_reference_id
                    except FormForGuardianship.DoesNotExist:
                        return HttpResponse(status=404)
                    guardian = FormForGuardianship.objects.get(id=guardian_id)
                    guardian.is_paid = True
                    checkout_session = CheckoutSessionStripe.objects.create(
                        checkout_session_id=session.id,
                        price_id=guardian.plan,
                        subscription_id=session.subscription,
                        customer_id=session.customer,
                        is_completed=True
                    )
                    guardian.pay_session = checkout_session
                    if guardian.user:
                        user = guardian.user
                        user.coins.increased(discount=10, payment_amount=guardian.plan.unit_amount,
                                             description=f'Подписка на {guardian.plan.name}')
                        user.save()
                    send_order_notification.delay(order_id=guardian_id, flag='guardian')
                    guardian.save()
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
            match payment_info.extra_param.type:
                case 'guardian':
                    guardian = FormForGuardianship.objects.get(id=payment_info.extra_param.id)
                    guardian.is_paid = payment_info.status
                    guardian.payment_method = payment_info.payment_method
                    send_order_notification.delay(order_id=guardian.id, flag='guardian')
                    guardian.save()
                    if guardian.user:
                        user = guardian.user
                        user.coins.increased(discount=10, payment_amount=user.plan.unit_amount,
                                             description=f'Подписка на {user.plan.name}')
                        user.save()
                case 'booking':
                    booking = Booking.objects.get(id=payment_info.extra_param.id)
                    booking.is_paid = payment_info.status
                    send_order_notification.delay(order_id=booking.id, flag='booking')
                    booking.save()
                    if booking.user and not booking.coupon and booking.bonuses != 0:
                        user = booking.user
                        user.coins.increased(discount=10, payment_amount=booking.cost,
                                             description=f'Бронь на {booking.date}, {booking.time}')
                        user.save()
        else:
            return HttpResponse(status=400)

    except Exception:
        return HttpResponse(status=400)

    return HttpResponse(200)
