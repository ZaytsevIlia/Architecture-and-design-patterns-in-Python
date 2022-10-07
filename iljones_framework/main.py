from pprint import pprint
from quopri import decodestring
from framework_requests import PostRequests, GetRequests


class PageNotFound404:
    def __call__(self, request):
        return '404 404', '404 PAGE Not Found'


class Framework:
    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}

        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().post_application(environ)
            request['data'] = Framework.decode_value(data)
            print(f'Нам пришёл post-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_application(environ)
            request['request_params'] = Framework.decode_value(request_params)
            print(f'Нам пришли GET-параметры:'
                  f' {Framework.decode_value(request_params)}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound404()

        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)
        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace('+', ' '), 'utf-8')
            val_decode_str = decodestring(val).decode('utf-8')
            new_data[k] = val_decode_str
        return new_data


# Логирующий WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class InfoApplication(Framework):
    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        print('----------Info mode----------')
        pprint(env)
        return self.application(env, start_response)


# Фейковый WSGI-application.
# На все запросы пользователя отвечает:
# 200 OK, Hello from Fake.

class FakeApplication(Framework):
    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from Fake']
