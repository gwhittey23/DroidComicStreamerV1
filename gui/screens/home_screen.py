from kivy.app import App
from kivy.uix.image import AsyncImage
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from comicstream.comicstreamerconn import ComicStreamerConnect
from comicstream.comic_data import ComicCollection, ComicBook
from gui.screens.custom_widgets import AppScreenTemplate, AppNavDrawer
from comicstream.url_get import CustomUrlRequest
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import ObjectProperty

from gui.theme_engine.label import MaterialLabel


class HomeScreeNavigationDrawer(AppNavDrawer):
    pass


class HomeScreen(AppScreenTemplate):
    def __init__(self,**kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.collection = None
    def build_home_screen(self):
        root = self
        app = App.get_running_app()

        root.toolbar.nav_button = ["md-keyboard-backspace",'']
        root.toolbar.add_action_button("md-book")
        root.toolbar.add_action_button("md-settings",lambda *x: app.open_settings())


        self.tile_data = [{'text': "Button 1", 'secondary_text': "With a secondary text"},
                          {'text': "Button 2", 'secondary_text': "With a secondary text"},
                          {'text': "Button 3", 'secondary_text': "With a secondary text"},
                          {'text': "Button 4", 'secondary_text': "With a secondary text"}]

        self.tile_single_data = [{'text': "Button 1"},
                                  {'text': "Button 2"},
                                  {'text': "Button 3"},
                                  {'text': "Button 4"}]

        self.tile_icon_data = [
                                {'icon': 'md-alarm', 'text': 'Alarm',
                                'secondary_text': "An alarm button",
                                'callback': self.toggle_nav},
                                {'icon': 'md-event', 'text': 'Event',
                                'secondary_text': "An event button",
                                'callback':self.toggle_nav},
                                {'icon':  'md-search', 'text': 'Search',
                                'secondary_text': "A search button",
                                'callback': self.toggle_nav},
                                {'icon': 'md-thumb-up', 'text': 'Like',
                                'secondary_text': "A like button",
                                'callback': self.toggle_nav}
                               ]
        self.build_recent_comics()
    def build_collection(self,req, results):
        print self.ids
        data = results
        new_collection = ComicCollection()
        for item in data['comics']:
            new_comic = ComicBook(item)
            new_collection.add_comic(new_comic)
        self.collection = new_collection.comics
        scroll = self.ids.recent_comics_scroll
        grid = RecentComicsOuterGrid(id='outtergrd')
        grid.bind(minimum_width=grid.setter('width'), )
        base_url = App.get_running_app().config.get('Server', 'url')
        for comic in self.collection:
            comic_name = '%s #%s'%(str(comic.series),str(comic.issue))
            src_thumb = comic.thumb_url
            inner_grid = RecentComicsInnerGrid(id='inner_grid'+str(comic.comic_id_number))
            comic_thumb = RecentComicsPageImage(source=src_thumb,id=str(comic.comic_id_number))
            comic_thumb.comic = comic
            comic_thumb.comics_collection = self.collection
            inner_grid.add_widget(comic_thumb)
            comic_thumb.bind(on_press=comic_thumb.click)
            smbutton = RecentComicsPagebntlbl(text=comic_name)
            inner_grid.add_widget(smbutton)
            grid.add_widget(inner_grid)
        scroll.add_widget(grid)

    def build_recent_comics(self):

        self.base_url = App.get_running_app().config.get('Server', 'url')
        recent_list  = "%s/comiclist?order=-added&per_page=10" % (self.base_url)
        req = CustomUrlRequest(recent_list,self.build_collection)

    def call_test(self):
        print self.collection



#<<<<Following are class for recent list>>>>>>>>>
class RecentComicsScroll(ScrollView):
    pass

class RecentComicsOuterGrid(GridLayout):
    pass

class RecentComicsPagebntlbl(Label):
    pass

class RecentComicsInnerGrid(GridLayout):
    pass

class RecentComicsPageImage(ButtonBehavior,AsyncImage):
    comic = ObjectProperty()
    comics_collection = ObjectProperty()
    def click(self,instance):
        app = App.get_running_app()
        app.root.current = 'comic_screen'
        comic_screen = app.root.get_screen('comic_screen')
        comic_screen.load_comic(self.comic,self.comics_collection)
#<<<<<<<<<<
