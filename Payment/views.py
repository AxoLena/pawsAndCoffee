import uuid
import stripe
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from currency_converter import CurrencyConverter
from yookassa import Configuration, Payment

from django.conf import settings

from Booking.models import Booking
from Cats.models import FormForGuardianship

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class PaymentForGuardianshipView(View):
    context = {
        'title': 'Способ оплаты',
    }

    def get(self, request):
        return render(request, 'payment/payment.html', context=self.context)

    def post(self, request):
        payment_type = request.POST.get('stripe', 'yookassa')
        if request.user.is_authenticated:
            guardian_queryset = FormForGuardianship.objects.filter(user=request.user)
        else:
            guardian_queryset = FormForGuardianship.objects.filter(session_key=request.session.session_key)
        guardian = guardian_queryset.latest('created_timestamp')
        try:
            match payment_type:
                case 'stripe':
                    session_data = {
                        'mode': 'subscription',
                        'success_url': request.build_absolute_uri(reverse('payment:success')),
                        'cancel_url': request.build_absolute_uri(reverse('payment:failed')),
                        'line_items': [{
                            'price': guardian.plan.price_id,
                            'quantity': 1,
                        }],
                        'client_reference_id': guardian.id,
                    }

                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)

                case 'yookassa':
                    idempotence_key = uuid.uuid4()
                    currency = 'RUB'
                    description = 'Подписка'
                    payment = Payment.create({
                        'amount': {
                            'value': guardian.amount_of_money,
                            'currency': currency
                        },
                        'confirmation': {
                            'type': 'redirect',
                            'return_url': request.build_absolute_uri(reverse('payment:success')),
                        },
                        'capture': True,
                        'test': True,
                        'description': description,
                        'extra_param': {'type': 'guardian', 'user_id': guardian.id},
                    }, idempotence_key)

                    confirmation_url = payment.confirmation.confirmation_url
                    return redirect(confirmation_url)

        except ValueError as e:
            pk = guardian.id
            instance = FormForGuardianship.objects.get(pk=pk)
            instance.delete()
            raise ValidationError(str(e))


class PaymentForBookingView(View):
    context = {
        'title': 'Способ оплаты',
    }

    def get(self, request):
        return render(request, 'payment/payment.html', context=self.context)

    def post(self, request):
        payment_type = request.POST.get('stripe', 'yookassa')
        if request.user.is_authenticated:
            booking_queryset = Booking.objects.filter(user=request.user)
        else:
            booking_queryset = Booking.objects.filter(session_key=request.session.session_key)
        booking = booking_queryset.latest('created_timestamp')
        cost = (booking.cost * booking.quantity)
        if booking.bonuses or booking.coupon:
            cost = cost - booking.bonuses if booking.bonuses > 0 else cost * (booking.coupon.discount / 100)
        try:
            match payment_type:
                case 'stripe':
                    c = CurrencyConverter()
                    session_data = {
                        'mode': 'payment',
                        'success_url': request.build_absolute_uri(reverse('payment:success')),
                        'cancel_url': request.build_absolute_uri(reverse('payment:failed')),
                        'line_items': [{
                            'price_data': {
                                'unit_amount': int(c.convert(float(cost), 'RUB', 'USD') * 100),
                                'currency': 'usd',
                                'product_data': {
                                    'name': f'Бронь на {booking.date}, {booking.time}'
                                }
                            },
                            'quantity': 1
                        }],
                        'client_reference_id': booking.id
                    }
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)

                case 'yookassa':
                    idempotence_key = uuid.uuid4()
                    currency = 'RUB'
                    description = f'Бронь на {booking.date}, {booking.time}'
                    payment = Payment.create({
                        'amount': {
                            'value': cost,
                            'currency': currency
                        },
                        'confirmation': {
                            'type': 'redirect',
                            'return_url': request.build_absolute_uri(reverse('payment:success')),
                        },
                        'capture': True,
                        'test': True,
                        'description': description,
                        'extra_param': {'type': 'booking', 'user_id': booking.id},
                    }, idempotence_key)

                    confirmation_url = payment.confirmation.confirmation_url
                    return redirect(confirmation_url)

        except ValueError:
            pk = booking.id
            instance = Booking.objects.get(pk=pk)
            instance.delete()
            return HttpResponse(status=404)


class PaymentAnswerSuccess(View):
    def get(self, request):
        messages.success(request, 'Оплата прошла успешно')
        return redirect(reverse('main:index'))


class PaymentAnswerFailed(View):
    def get(self, request):
        messages.warning(request, 'Ошибка!\n Не удалось произвести оплату')
        return redirect(reverse('main:index'))


class DeleteSubscriptionView(View):
    def post(self, request):
        guardian_id = request.POST.get('guardian_id')
        guardian = FormForGuardianship.objects.get(id=guardian_id)
        if guardian:
            if not guardian.payment_method:
                subscription_id = guardian_id.pay_session.subscription_id
                try:
                    subscription = stripe.Subscription.delete(subscription_id)
                    return JsonResponse({'data': subscription}, status=200)
                except Exception as e:
                    return ValidationError(str(e))
            else:
                guardian.payment_method = None
                guardian.save()
                return JsonResponse({'data': 'payment_method is Null'}, status=200)

        return JsonResponse({'error': 'guardian is not found'}, status=400)
