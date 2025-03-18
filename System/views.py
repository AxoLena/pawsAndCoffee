from django.shortcuts import render


def tr_handler404(request, exception):
    context = {
        'title': 'Страница не найдена: ошибка 404'
    }
    return render(request=request, template_name='system/errors/error_page404.html', status=404, context=context)


def tr_handler403(request, exception):
    context = {
        'title': 'Ошибка доступа: ошибка 403'
    }
    return render(request=request, template_name='system/errors/error_page403.html', status=403, context=context)


def tr_handler500(request):
    context = {
        'title': 'Ошибка сервера: ошибка 500'
    }
    return render(request=request, template_name='system/errors/error_page500.html', status=500, context=context)
