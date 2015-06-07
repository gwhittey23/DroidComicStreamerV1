from kivy.uix.screenmanager import Screen
from kivy.app import App
from gui.theme_engine.theme import ThemeBehaviour
from gui.navigationdrawer import NavigationDrawer
from kivy.base import EventLoop
from kivy.metrics import dp
from kivy.properties import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import ButtonBehavior
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.uix.popup import PopupException


class AppNavDrawer(ThemeBehaviour,NavigationDrawer):
    header_img = StringProperty()

    _header_bg = ObjectProperty()
    _bl_items = ObjectProperty()

class AppScreenTemplate(Screen):
    tile_icon_data = ListProperty()
    test_icon_data = ListProperty()
    tile_link_data = ListProperty()
    def toggle_nav(self):

        if self.nav.state != "open":
            return
        self.nav.toggle_state()

    def on_leave(self):
        app = App.get_running_app()
        app.manager.last_screen = self

