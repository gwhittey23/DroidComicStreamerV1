from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from comic_data import ComicCollection,ComicBook
from comicstream.url_get import CustomUrlRequest


class Bob(object):
    pass
class ComicStreamerConnect(object):

    def __init__(self):
        self.base_url = App.get_running_app().config.get('Server', 'url')


     # def get_server_data(self):
     #     get_series_url = "%s/comiclist?order=added&per_page=10" % (self.base_url, , i)

    def get_recent_comics(self):
        def got_data(data):
            recent_collection = ComicCollection()
            comic = ComicBook()
            'brake data into sinle comics'
            for item in data['comics']:
                for key, value in item.items():
                    comic_prop =comic_prop + (('%s=%s,') %(key,value))
                new_comic =ComicBook(comic_prop)
                recent_collection.add_comic(new_comic)
            return recent_collection
        recent_list  = "%s/comiclist?order=added&per_page=10" % (self.base_url)
        req = CustomUrlRequest(recent_list,got_data)