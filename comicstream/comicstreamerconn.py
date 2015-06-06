from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from comic_data import ComicCollection,ComicBook

from comicstream.url_get import CustomUrlRequest


class Bob(object):
    pass
class ComicStreamerConnect(object):

    def __init__(self):

        self.data = ''

     # def get_server_data(self):
     #     get_series_url = "%s/comiclist?order=added&per_page=10" % (self.base_url, , i)

    def get_recent_comics(self):

        def got_data(req, results):
            self.data = results
        self.base_url = App.get_running_app().config.get('Server', 'url')

        recent_list  = "%s/comiclist?order=-added&per_page=10" % (self.base_url)
        print recent_list
        req = CustomUrlRequest(recent_list,got_data,debug=True)
