from wsgiref.simple_server import make_server
from iljones_framework.main import Framework, InfoApplication, FakeApplication
from urls import fronts
from views import routes

application = Framework(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
