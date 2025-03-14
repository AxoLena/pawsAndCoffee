from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from pawsAndCoffee import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api-auth/', include('rest_framework.urls')),

    path('', include('Main.urls', namespace='main')),
    path('user/', include('Users.urls', namespace='users')),
    path('cats/', include('Cats.urls', namespace='cats')),
    path('calendar/', include('Booking.urls', namespace='booking')),
    path('payment/', include('Payment.urls', namespace='payment')),
    path('bonus/', include('Bonuses.urls', namespace='bonuses'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
