__version__ = '1.0000000018'
DEBUG = True
import kivy
kivy.require('1.9.1')
if DEBUG:
    from kivy.config import Config
    print 'setting windows size'
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '1024')
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from data.settingsjson   import settings_json_server,settings_json_dispaly
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from kivy.uix.actionbar import ActionBar
from gui.widgets.actionbars import TopActionBar
from gui.screens.comic_screen import ComicScreen
from gui.screens.home_screen import HomeScreen
from gui.screens.comic_shelf_screen import ComicShelfScreen
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
#from csvdb.csvdroid_db import build_db
from kivy.clock import Clock

from kivy.logger import Logger
from kivy.loader import Loader
from kivy.lang import Factory
from kivy.core.window import Window
from functools import partial
from kivy.graphics.transformation import Matrix
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty,StringProperty
from gui.theme_engine.toolbar import Toolbar
#from gui.theme_engine.navigationdrawer import NavigationDrawer
from gui.theme_engine.button import RaisedButton, FlatButton, FloatingActionButton
from gui.theme_engine.dialog import Dialog
from gui.theme_engine.label import MaterialLabel
from gui.theme_engine.theme import ThemeBehaviour, ThemeManager
from gui.theme_engine import images_path
from gui.theme_engine.list import MaterialList, TextTile
from gui.theme_engine.selectioncontrols import MaterialCheckBox, MaterialSwitch
from helpers import bind_to_rotation
from kivy.modules import keybinding
from kivy.app import App

class AppScreenManager(ScreenManager):
    last_screen = ObjectProperty()
    def __init__(self,**kwargs):
        super(AppScreenManager, self).__init__(**kwargs)
    def load_comic_screen(self,comic_number=1844):
        home_screen = self.get_screen('home_screen')
        comic_number = int(home_screen.ids['txt1'].text)
        print comic_number
        self.get_screen('comic_screen').load_comic(comic_number)
        self.current = 'comic_screen'

    def load_comic_shelf_screen(self):
        comic_self_screen = self.get_screen('comic_shelf_screen')
        comic_self_screen.load_series()
        self.current = 'comic_shelf_screen'

    def _go_home_screen(self,instance):
           self.current = 'home_screen'
    def open_last_screen(self):
        self.current = self.last_screen.name

class MainApp(App):
    version = StringProperty()
    version = __version__
    theme_cls = ThemeManager()

    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.theme_cls.primary_palette = 'Grey'
        self.theme_cls.accent_palette = 'Teal'
        self.theme_cls.theme_style = 'Dark'
    def build(self):
        self.manager = AppScreenManager()
        self.manager.get_screen('home_screen').build_home_screen()
        comic_shelf_screen =self.manager.get_screen('comic_shelf_screen')
        Clock.schedule_once(comic_shelf_screen.build_comic_shelf_screen,.05)

        keybinding.start(Window, App)
        return self.manager


    def build_config(self, config):
        config.setdefaults('Server', {
            'url': 'http://',
            'storagedir': self.user_data_dir,
            'max_height': 0
            })

        config.setdefaults('Display', {
            'mag_glass_size': 200,
            'right2left':       0,
            'dblpagesplit': self.user_data_dir,

            })


    def build_settings(self, settings):
        settings.add_json_panel('Server Settings',
                                self.config,
                                data=settings_json_server)
        settings.add_json_panel('Display Settings',
                                self.config,
                                data=settings_json_dispaly)

    def on_config_change(self, config, section,
                         key, value):
        print config, section, key, value

    def on_pause(self):
      # Here you can save data if needed
         return True

    def on_resume(self):
      # Here you can check if any data needs replacing (usually nothing)
        pass

    def on_stop(self):
        pass
#        self.manager.get_screen('comic_screen')._abort_download()


if __name__ == '__main__':
    MainApp().run()