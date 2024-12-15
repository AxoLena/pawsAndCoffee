import uuid

import requests
import stripe
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from currency_converter import CurrencyConverter
from yookassa import Configuration, Payment

from django.conf import settings

from Users.models import User
from Cats.models import FormForGuardianship

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class PaymentForGuardianshipView(View):
    context = {
        'title': 'Способ оплаты',
    }

    def get_guardian(self):
            url = 'http://127.0.0.1:8000/cats/api/guardianship/'
            response = requests.get(url)
            user = response.json()
            return user['post'][-1]

    def get(self, request):
        guardian_pk = self.get_guardian()
        guardian = User.objects.get(pk=guardian_pk)
        session_key = request.session.session_key
        if guardian['session_key'] == session_key:
            return render(request, 'payment/payment.html', context=self.context)
        elif guardian_pk['user'] == request.user.pk:
            return render(request, 'payment/payment.html', context=self.context)
        else:
            messages.warning(self.request, 'На сервере произошла ошибка!\n Введите данные заново')
            pk = guardian['id']
            instance = FormForGuardianship.objects.get(pk=pk)
            instance.delete()
            return redirect(request, reverse('cats:guardianship'))

    def post(self, request):
        payment_type = request.POST.get('stripe', 'yookassa')
        guardian_pk = self.get_guardian()
        guardian = User.objects.get(pk=guardian_pk)
        try:
            match payment_type:
                case 'stripe':
                    c = CurrencyConverter()
                    session_data = {
                        'mode': 'payment',
                        'success_url': request.build_absolute_uri(reverse('payment:success')),
                        'cancel_url': request.build_absolute_uri(reverse('payment:failed')),
                        'line_items': []
                    }

                    session_data['line_items'].append({
                        'price_data': {
                            'unit_amount': int(c.convert(float(guardian['amount_of_money']), 'RUB', 'USD') * 100),
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Подписка'
                            }
                        },
                        'quantity': 1
                    })

                    session_data['client_reference_id'] = guardian['id']
                    session = stripe.checkout.Session.create(**session_data)
                    return redirect(session.url, code=303)

                case 'yookassa':
                    idempotence_key = uuid.uuid4()
                    currency = 'RUB'
                    description = 'Подписка'
                    payment = Payment.create({
                        'amount': {
                            'value': guardian['amount_of_money'],
                            'currency': currency
                        },
                        'confirmation': {
                            'type': 'redirect',
                            'return_url': request.build_absolute_uri(reverse('payment:success')),
                        },
                        'capture': True,
                        'test': True,
                        'description': description,
                    }, idempotence_key)

                    confirmation_url = payment.confirmation.confirmation_url
                    return redirect(confirmation_url)

        except ValueError:
            pk = guardian['id']
            instance = FormForGuardianship.objects.get(pk=pk)
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