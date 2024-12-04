from django.urls import path

from Payment.webhooks import stripe_webhook
from Payment.views import PaymentForGuardianshipView, PaymentAnswerSuccess, PaymentAnswerFailed

app_name = 'payment'

urlpatterns = [
    path('', PaymentForGuardianshipView.as_view(), name='select-guardianship'),
    path('success/', PaymentAnswerSuccess.as_view(), name='success'),
    path('failed/', PaymentAnswerFailed.as_view(), name='failed'),
    path('webhook-stripe/', stripe_webhook)
]