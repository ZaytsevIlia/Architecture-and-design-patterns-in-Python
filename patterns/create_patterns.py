from copy import deepcopy
from quopri import decodestring


class User:
    pass


class Driver(User):
    pass


class Student(User):
    pass


class UserFactory:
    types = {
        'driver': Driver,
        'student': Student,
    }

    # Порождающий патерн
    # Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class TrackPrototype:
    def clone(self):
        return deepcopy(self)


class Track(TrackPrototype):
    def __init__(self, name, mode):
        self.name = name
        self.mode = mode
        self.mode.tracks.append(self)


class MoscowTrack(Track):
    pass


class SPeterTrack(Track):
    pass


class SochiTrack(Track):
    pass


class KazanTrack(Track):
    pass


class GrozniyTrack(Track):
    pass


class TrackFactory:
    types = {
        'moscowtrack': MoscowTrack,
        'spetertrack': SPeterTrack,
        'sochitrack': SochiTrack,
        'kazantrack': KazanTrack,
        'grozniytrack': GrozniyTrack,
    }

    # Порождающий патерн
    # Фабричный метод
    @classmethod
    def create(cls, type_, name, mode):
        return cls.types[type_](name, mode)


class Mode:
    auto_id = 0

    def __init__(self, name, mode):
        self.id = Mode.auto_id
        Mode.auto_id += 1
        self.name = name
        self.mode = mode
        self.tracks = []

    def tracks_count(self):
        result = len(self.tracks)
        if self.mode:
            result += self.mode.tracks_count()
        return result


class Engine:
    def __init__(self):
        self.modes = []
        self.drivers = []
        self.students = []
        self.tracks = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_track(type_, name, mode):
        return TrackFactory.create(type_, name, mode)

    def get_track(self, name):
        for item in self.tracks:
            if item.name == name:
                return item
        return None

    @staticmethod
    def create_mode(name, mode=None):
        return Mode(name, mode)

    def find_mode_by_id(self, id):
        for item in self.modes:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет режима с id = {id}')

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace('+', ' '), 'utf-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('utf-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]
