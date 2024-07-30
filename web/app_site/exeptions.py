import traceback
from datetime import datetime
from django.http import JsonResponse
from django.views import View
import logging

logging.basicConfig(filename="log.log")
JSON_DUMPS_PARAMS = {"ensure_ascii": False}


def ret(json_object, status=200):
    """ Отдаем JSON с правильным HTTP заголовками и в читаемом виде
    в браузере в случае с кирилицей"""
    return JsonResponse(
        json_object,
        status=status,
        safe=not isinstance(json_object, list),
        json_dumps_params=JSON_DUMPS_PARAMS
    )


def error_response(exception):
    """форматирует HTTP ответ с описанием ошибки и  Traceback"""
    # trace = ''
    # if DEBUG:
    trace = traceback.format_exc()
    res = {"errorMessage": str(exception), "tracerback": trace}
    return ret(res, status=400)


class BaseClassExeption(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except BaseException as e:
            logging.warning("===========================================================")
            logging.warning("ВРЕМЯ:     " + str(datetime.now()))
            logging.warning("ОШИБКА:        "+str(e))
            logging.warning("ТРЭЙСБЭК:     " + traceback.format_exc())
            logging.warning("============================================================")
            return JsonResponse({'message': "ОШИБКА ДАННЫХ!", 'comments': str(e)}, status=400, safe=False,
                                json_dumps_params=JSON_DUMPS_PARAMS)
        return response
