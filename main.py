__version__ = '1.0000000004'
DEBUG = True
import kivy
kivy.require('1.8.0')
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

from kivy.app import App

class AppScreenManager(ScreenManager):

    def load_comic_screen(self,comic_number=1844):
        comic_number = int(self.ids['txt1'].text)
        print comic_number
        self.get_screen('comic_screen').load_comic(comic_number)
        self.current = 'comic_screen'



class MainApp(App):
    def build(self):
        manager = AppScreenManager()
        return manager

    def build_config(self, config):
        config.setdefaults('Server', {
            'url': 'http://',
            'storagedir': self.user_data_dir
            })

        config.setdefaults('Display', {
            'mag_glass_size': 200,
            'dblpagesplit': self.user_data_dir
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


if __name__ == '__main__':
    MainApp().run()