from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from System.views import tr_handler500, tr_handler403, tr_handler404
from pawsAndCoffee import settings

handler403 = tr_handler403
handler404 = tr_handler404
handler500 = tr_handler500

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
    urlpatterns += [
        re_path(r'^403$', TemplateView.as_view(template_name='system/errors/error_page403.html')),
        re_path(r'^404$', TemplateView.as_view(template_name='system/errors/error_page404.html')),
        re_path(r'^500$', TemplateView.as_view(template_name='system/errors/error_page500.html')),
    ]
