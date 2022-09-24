from iljones_framework.templator import render
from patterns.create_patterns import Engine

site = Engine()

class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.modes)


class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


class AnotherPage:
    def __call__(self, request):
        return '200 OK', render('another_page.html', date=request.get('date', None))


# Контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Контроллер список трасс
class TrackList:
    def __call__(self, request):
        try:
            mode = site.find_mode_by_id(int(request['request_params']['id']))
            return '200 OK', render('track_list.html',
                                    objects_list=mode.tracks,
                                    name=mode.name,
                                    id=mode.id)
        except KeyError:
            return '200 OK', 'Не выбрано ни одной трассы'


# Контроллер создать трассу
class CreateTrack:
    mode_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            mode = None
            if self.mode_id != -1:
                mode = site.find_mode_by_id(int(self.mode_id))

                track = site.create_track('moscowtrack', name, mode)
                site.tracks.append(track)

            return '200 OK', render('track_list.html',
                                    objects_list=mode.tracks,
                                    name=mode.name,
                                    id=mode.id)
        else:
            try:
                self.mode_id = int(request['request_params']['id'])
                mode = site.find_mode_by_id(int(self.mode_id))

                return '200 OK', render('choise_track.html',
                                        name=mode.name,
                                        id=mode.id)
            except KeyError:
                return '200 OK', 'Не выбрано ни одной трассы'


# Контроллер список режимов
class ModeList:
    def __call__(self, request):
        return '200 OK', render('mode_list.html', objects_list=site.modes)


# Контроллер создать режим
class CreateMode:
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            mode_id = data.get('mode_id')

            mode = None
            if mode_id:
                mode = site.find_mode_by_id(int(mode_id))

            new_mode = site.create_mode(name, mode)
            site.modes.append(new_mode)

            return '200 OK', render('index.html', objects_list=site.modes)

        else:
            modes = site.modes
            return '200 OK', render('choise_mode.html', modes=modes)




# Контроллер копировать трассу
class CopyTrack:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_track = site.get_track(name)

            if old_track:
                new_name = f'copy_{name}'
                new_track = old_track.clone()
                new_track.name = new_name
                site.tracks.append(new_track)

            return '200 OK', render('track_list.html',
                                    objects_list=site.tracks,
                                    name=new_track.mode.name)
        except KeyError:
            return '200 OK', 'Не выбрано ни одной трассы'




















