from iljones_framework.templator import render
from patterns.create_patterns import Engine
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import SMSNotifier, EmailNotifier, BaseSerializer, ListView, CreateView

site = Engine()
sms_notifier = SMSNotifier()
email_notifier = EmailNotifier()

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.modes)


@AppRoute(routes=routes, url='/contact/')
class Contact:
    @Debug(name='Contact')
    def __call__(self, request):
        return '200 OK', render('contact.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


@AppRoute(routes=routes, url='/another_page/')
class AnotherPage:
    @Debug(name='AnotherPage')
    def __call__(self, request):
        return '200 OK', render('another_page.html', date=request.get('date', None))


# Контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# Контроллер список трасс
@AppRoute(routes=routes, url='/track_list/')
class TrackList:
    @Debug(name='TrackList')
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
@AppRoute(routes=routes, url='/choise_track/')
class CreateTrack:
    mode_id = -1

    @Debug(name='CreateTrack')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)

            mode = None
            if self.mode_id != -1:
                mode = site.find_mode_by_id(int(self.mode_id))

                track = site.create_track('moscowtrack', name, mode)

                track.observers.append(email_notifier)
                track.observers.append(sms_notifier)

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
@AppRoute(routes=routes, url='/mode_list/')
class ModeList:
    @Debug(name='ModeList')
    def __call__(self, request):
        return '200 OK', render('mode_list.html', objects_list=site.modes)


# Контроллер создать режим
@AppRoute(routes=routes, url='/choise_mode/')
class CreateMode:
    @Debug(name='CreateMode')
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
@AppRoute(routes=routes, url='/track_copy/')
class CopyTrack:
    @Debug(name='CopyTrack')
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


@AppRoute(routes=routes, url='/student_list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student_list.html'


@AppRoute(routes=routes, url='/create_student/')
class StudentCreateView(CreateView):
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)


@AppRoute(routes=routes, url='/add_student/')
class AddStudentByTrackCreateView(CreateView):
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['tracks'] = site.tracks
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        track_name = data['track_name']
        track_name = site.decode_value(track_name)
        track = site.get_track(track_name)
        student_name = data['student_name']
        student_name = site.decode_value(student_name)
        student = site.get_student(student_name)
        track.add_student(student)


@AppRoute(routes=routes, url='/api/')
class TrackApi:
    @Debug(name='TrackApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.tracks).save()
