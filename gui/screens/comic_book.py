from kivy.logger import Logger
from kivy.properties import NumericProperty,ObjectProperty
from gui.widgets.custom_widgets import AppScreenTemplate
from kivy.uix.image import AsyncImage

from kivy.uix.scatterlayout import ScatterLayout
import random
from kivy.app import App



class ComicBookScreen(AppScreenTemplate):
    def load_comic_book(self,comic_book_number):

        comic_book_carousel = self.ids['comic_book_carousel']
        comic_book_carousel.clear_widgets()
        number_pages = 20
        base_url = App.get_running_app().config.get('Server', 'url')
        max_height = App.get_running_app().config.get('Server', 'max_height')
        for i in range(0, number_pages):
            comic_book_scatter = ComicBookPageScatter(id='comic_scatter'+str(i))
            src_full = "%s/comic/%d/page/%d?max_height=%d#.jpg" % (base_url, comic_book_number, i,int(max_height))
            comic_book_image = ComicBookPageImage(source=src_full,id='pi_'+str(i))
            comic_book_scatter.add_widget(comic_book_image)
            comic_book_carousel.add_widget(comic_book_scatter)
    #Just here to test
    def load_random_comic(self):
        comic_number = random.randint(2660, 2780)
        self.load_comic_book(comic_number)
class ComicBookPageScatter(ScatterLayout):

    image_src = ObjectProperty()


class ComicBookPageImage(AsyncImage):
    pass

