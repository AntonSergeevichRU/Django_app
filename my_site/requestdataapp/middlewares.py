import time

from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_on_request_middleware(get_response):
    print('initial call')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META.get('HTTP_USER_AGENT')
        response = get_response(request)
        print('after get response')
        return response
    return middleware


class CountRequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_count = 0
        self.response_count = 0
        self.exception_count = 0
        self.request_time = {}

    def __call__(self, request: HttpRequest):
        time_delay = 0

        if request.META.get('REMOTE_ADDR') in self.request_time:
            if (round(time.time(), 0)) - self.request_time[request.META.get('REMOTE_ADDR')] < time_delay:
                print('С прошлого запроса прошло менее 5 сек')
                return render(request, 'requestdataapp/request_error.html')
            else:
                self.request_time[request.META.get('REMOTE_ADDR')] = round(time.time(), 0)
        else:
            print(request.META.get('REMOTE_ADDR'),'первый запрос', round(time.time(), 0))
            self.request_time[request.META.get('REMOTE_ADDR')] = round(time.time(), 0)


        self.request_count += 1
        print('request count:', self.request_count)

        response = self.get_response(request)
        self.response_count += 1
        print('response_count:', self.response_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exception_count += 1
        print('exception_count:', self.exception_count)


