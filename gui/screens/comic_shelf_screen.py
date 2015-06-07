from kivy.properties import StringProperty
from kivy.uix.carousel import Carousel
from kivy.properties import ListProperty, ObjectProperty
#from theme_engine.navigationdrawer import NavigationDrawer
from gui.theme_engine.theme import ThemeManager
from kivy.app import App
from gui.widgets.custom_widgets import AppScreenTemplate,AppNavDrawer


class ComicShelfCarousel(Carousel):
    pass

class ComicShelfScreen(AppScreenTemplate):
    theme_cls = ThemeManager()
    tile_data = ListProperty([])
    tile_single_data = ListProperty([])
    tile_icon_data = ListProperty()
    tile_avatar_data = ListProperty()
    nav = ObjectProperty()
    def __init__(self, **kwargs):
        super(ComicShelfScreen, self).__init__(**kwargs)
        display_mode = StringProperty()




    def load_mode(self,display_mode):
        print display_mode
        if display_mode == 'Series':self.load_series()

    def _go_home_screen(self):
        app = App.get_running_app()
        app.manager.current = 'home_screen'

    def build_comic_shelf_screen(self,instance):
        root = self
        app = App.get_running_app()
        root.toolbar.nav_button = ["md-keyboard-backspace",lambda *x: app.manager.open_last_screen()]
        root.toolbar.add_action_button("md-refresh")
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
    def load_series(self):
        pass


class LibraryScreeNavigationDrawer(AppNavDrawer):
    pass

