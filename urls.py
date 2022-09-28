from datetime import date
from views import Index, About, AnotherPage, Contact, CreateMode, CreateTrack, ModeList, TrackList, CopyTrack


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/another_page/': AnotherPage(),
    '/contact/': Contact(),
    '/choise_mode/': CreateMode(),
    '/choise_track/': CreateTrack(),
    '/mode_list/': ModeList(),
    '/track_list/': TrackList(),
    '/track_copy/': CopyTrack(),
}
