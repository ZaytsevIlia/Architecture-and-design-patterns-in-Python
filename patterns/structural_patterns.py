from time import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls()


class Debug:
    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        def timeit(method):
            def timed(*args, **kwargs):
                ts = time()  # time start
                result = method(*args, **kwargs)
                te = time()  # time end
                delta = te - ts

                print(f'debug ---> Функция: {self.name} - время выполнения: {delta:2.2f} сек.')
                return result

            return timed

        return timeit(cls)
