from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """

    env = Environment()

    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)

    # находим шаблон в окружении
    template = env.get_template(template_name)

     # рендерим шаблон с параметрами
    return template.render(**kwargs)
