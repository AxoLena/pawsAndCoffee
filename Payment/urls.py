from django.urls import path

from Payment.webhooks import stripe_webhook
from Payment.views import PaymentForGuardianshipView, PaymentForBookingView, PaymentAnswerSuccess, PaymentAnswerFailed

app_name = 'payment'

urlpatterns = [
    path('guardianship/', PaymentForGuardianshipView.as_view(), name='select-guardianship'),
    path('booking/', PaymentForBookingView.as_view(), name='select-booking'),
    path('success/', PaymentAnswerSuccess.as_view(), name='success'),
    path('failed/', PaymentAnswerFailed.as_view(), name='failed'),
    path('webhook-stripe/', stripe_webhook)
]