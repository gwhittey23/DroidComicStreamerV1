from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.scatter import Scatter
from kivy.properties import ObjectProperty, StringProperty
import random
from kivy.logger import Logger
from kivy.uix.label import Label
from functools import partial
from kivy.loader import Loader
from kivy.properties import NumericProperty
from kivy.uix.carousel import Carousel
from kivy.graphics.transformation import Matrix
from kivy.core.window import Window
from gui.widgets.custom_widgets import AppScreenTemplate
from gui.theme_engine.dialog import Dialog
from kivy.uix.image import AsyncImage
from kivy.metrics import dp
from kivy.clock import Clock
from gui.widgets.custom_effects import RectangularRippleBehavior
from comicstream.comic_data import ComicCollection, ComicBook
from comicstream.url_get import CustomUrlRequest
# from memory_profiler import profile
import gc

class ComicScreen(AppScreenTemplate):
    minmove = StringProperty()
    move_state = StringProperty()
    ab_state = StringProperty()
    comic_id = NumericProperty()
    comic = ObjectProperty()
    comics_collection2 = ObjectProperty()
    next_comic = ObjectProperty()
    prev_comic = ObjectProperty()
    scroller = ObjectProperty()

    def __init__(self,**kwargs):
        super(ComicScreen, self).__init__(**kwargs)
    #     self.move_state = 'open'
    #     self.ab_state = 'closed'
    # #

    def on_leave(self):
        app = App.get_running_app()
        app.manager.last_screen = self


    def comicscreen_open_collection_popup(self):
        self.top_pop.open()


    def build_top_list(self):
        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False,id='page_thumb_scroll')
        self.top_pop = Popup(id='page_pop',title='Pages', content=scroll, pos_hint ={'y': .7},size_hint = (1,.33))
        grid = GridLayout(rows=1, size_hint=(None,None),spacing=5,padding_horizontal=5,id='outtergrd')
        grid.bind(minimum_width=grid.setter('width'))
        for comic in self.comics_collection.comics:
            comic_name = '%s #%s'%(str(comic.series),str(comic.issue))
            src_thumb = comic.thumb_url
            inner_grid = NextComicsInnerGrid(id='inner_grid'+str(comic.comic_id_number))
            comic_thumb = NextComicImage(source=src_thumb,id=str(comic.comic_id_number),nocache=True)
            comic_thumb.comic = comic
            comic_thumb.comics_collection = self.comics_collection
            inner_grid.add_widget(comic_thumb)
            comic_thumb.bind(on_release=self.top_pop.dismiss)
            comic_thumb.bind(on_release=comic_thumb.click)

            smbutton = NextComicsPagebntlbl(text=comic_name)
            inner_grid.add_widget(smbutton)
            grid.add_widget(inner_grid)
        scroll.add_widget(grid)
    def load_random_comic(self):
        def got_data(req,results):

            data = results

            print data
            new_collection = ComicCollection()

            new_comic = ComicBook(data['comics'][0])
            new_collection.add_comic(new_comic)
            self.load_comic(new_comic,new_collection)
        comic_number = random.randint(2660, 2780)
        self.base_url = App.get_running_app().config.get('Server', 'url')
        recent_list  = "%s/comic/%d" % (self.base_url,comic_number)
        req = CustomUrlRequest(recent_list,
                               got_data,

                               timeout = 15,
                               )
    # @profile()
    def load_comic(self,comic,comics_collection):
        self.minmove = 'off'

        Loader.pool.tasks.queue.clear()
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        carousel.clear_widgets()
        gc.collect()
        self.comic = comic
        self.comics_collection = comics_collection
        print comics_collection
        comic_number = comic.comic_id_number
        page_count = comic.page_count
        m_win_x = Window.width
        m_win_y = Window.height
        proxyImage = ''
        base_url = App.get_running_app().config.get('Server', 'url')
        max_height = App.get_running_app().config.get('Server', 'max_height')
        scroll = ScrollView( size_hint=(1,1), do_scroll_x=True, do_scroll_y=False,id='page_thumb_scroll')
        self.thumb_pop = Popup(id='page_pop',title='Pages', content=scroll, pos_hint ={'y': .0001},size_hint = (1,.33))
        self.scroller = scroll
        outer_grid = GridLayout(rows=1, size_hint=(None,None),spacing=5,padding_horizontal=5,id='outtergrd')
        outer_grid.bind(minimum_width=outer_grid.setter('width'))

        for i in range(0, page_count):
            src_full = "%s/comic/%d/page/%d?max_height=%d#.jpg" % (base_url, comic_number, i,int(max_height))
            src_thumb = "%s/comic/%d/page/%d?max_height=200#.jpg" % (base_url, comic_number, i)
            scatter = ComicPageScatter(id='comic_scatter'+str(i))

            comic_page_image = ComicPageImage(source=src_full, _index=i,id='pi_'+str(i),parent_id=scatter.id,nocache=True)

            scatter.add_widget(comic_page_image)
            carousel.add_widget(scatter)
            c_index =  len(carousel.slides)
            comic_page_image.car_index = c_index
            inner_grid = ThumbPopPageInnerGrid(id='inner_grid'+str(i))

            page_thumb = ThumbPopPageImage(source=src_thumb,id=scatter.id,_index=i)
            inner_grid.add_widget(page_thumb)
            page_thumb.bind(on_release=page_thumb.click)
            smbutton = ThumbPopPagebntlbl(text='P%s'%str(i+1))
            inner_grid.add_widget(smbutton)
            outer_grid.add_widget(inner_grid)
            # proxyImage = Loader.image(src_full,nocache=True)
            # proxyImage.bind(on_load=partial(comic_page_image._new_image_downloaded, scatter,outer_grid,comic_number))

        scroll.add_widget(outer_grid)
        x = 0

        print len(self.comics_collection.comics)
        if len(self.comics_collection.comics)>1:
            self.build_top_list()
            self.next_comic = self.get_next_comic()
            self.prev_comic = self.get_prev_comic()
            self.build_next_comic_dialog()
            self.build_prev_comic_dialog()
            self.ids['btn_collection'].disabled = False
        else:
            self.ids['btn_collection'].disabled = True

    def _open_mag_glass(self):
        my_carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']

        scatter_w = my_carousel.current_slide

        scatter_w.open_mag_glass()

    def scroll_to_page(self, *largs):
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        current_slide = carousel.current_slide
        for child in self.walk():
            if child.id == current_slide.id:
                Logger.debug('child is %s == slide == %s'%(child.id,current_slide.id ))
                current_page = child

        for child in self.thumb_pop.walk():
            Logger.debug('%s:%s'% (child,child.id))
            if child.id == 'page_thumb_scroll':
                scroller = child
                for grandchild in scroller.walk():
                    Logger.debug('--------%s:%s'% (grandchild,grandchild.id))
                    if grandchild.id == current_page.id:
                        target_thumb = grandchild
                        Logger.debug('target_thumb: %s'%target_thumb)
                        self.scroller.scroll_to(target_thumb,padding=10, animate=True)



        Logger.debug('self.scroller.id :%s'%self.scroller.id)

    def comicscreen_open_pagescroll_popup(self):

        self.thumb_pop.open()
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        current_slide = carousel.current_slide
        for child in self.walk():
            if child.id == current_slide.id:
                Logger.debug('child is %s == slide == %s'%(child.id,current_slide.id ))
                current_page =child

        for child in self.thumb_pop.walk():
            Logger.debug('%s:%s'% (child,child.id))
            if child.id == 'page_thumb_scroll':
                scroller = child
                for grandchild in scroller.walk():
                    Logger.debug('--------%s:%s'% (grandchild,grandchild.id))
                    if grandchild.id == current_page.id:
                        target_thumb = grandchild
                        Logger.debug('target_thumb: %s'%target_thumb)
                        self.scroller.scroll_to(target_thumb,padding=10, animate=True)


    def _cal_id(self):
       carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
       carousel.clear_widgets()
       gc.collect()


    def _abort_download(self):
        '''Stop the image from downloading'''
        Loader.stop()

    def load_next_slide(self,btn):
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        if carousel.index == len(carousel.slides)-1:
            self.open_next_dialog()
        else:
            carousel.load_next()
        btn.disabled = True
        Clock.schedule_once(btn.enable_me, .5)

    def load_prev_slide(self,btn):
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        print len(carousel.slides)
        if carousel.index == 0:
            self.open_prev_dialog()
        else:
            carousel.load_previous()
        btn.disabled = True
        Clock.schedule_once(btn.enable_me, .5)
    def get_next_comic(self):
        comics_collection = self.comics_collection.comics
        comic = self.comic
        index = comics_collection.index(comic) # first index where x appears

        if index >= len(comics_collection)-1:
            next_comic = comics_collection[index]
        else:
            next_comic = comics_collection[index+1]
        return next_comic

    def build_next_comic_dialog(self):
        ''' Make popup showing cover for next comic'''
        base_url = App.get_running_app().config.get('Server', 'url')
        comic = self.next_comic
        Logger.debug('self.next_comic.comic_id_number: %s'%self.next_comic.comic_id_number)
        Logger.debug('comic_id_number: %s'%comic.comic_id_number)

        comic_name = '%s #%s'%(str(comic.series),str(comic.issue))
        src_thumb = comic.thumb_url
        inner_grid = NextComicsInnerGrid(id='inner_grid'+str(comic.comic_id_number))
        comic_thumb = NextComicImage(source=self.next_comic.thumb_url,id=str(comic.comic_id_number),nocache=True)

        comic_thumb.comic = self.next_comic
        comic_thumb.comics_collection = self.comics_collection
        inner_grid.add_widget(comic_thumb)

        smbutton = NextComicsPagebntlbl(text=comic_name)
        inner_grid.add_widget(smbutton)
        content = inner_grid
        self.next_dialog = Dialog(title="Load Next",
                             content=content,
                             size_hint=(.3, .3),
                             height=dp(250),
                             auto_dismiss=True)
        comic_thumb.bind(on_release=self.next_dialog.dismiss)
        comic_thumb.bind(on_release=comic_thumb.click)

    def open_next_dialog(self):
         self.next_dialog.open()

    def build_prev_comic_dialog(self):
        base_url = App.get_running_app().config.get('Server', 'url')
        prev_comic = self.prev_comic
        comic_name = '%s #%s'%(str(prev_comic.series),str(prev_comic.issue))
        src_thumb = prev_comic.thumb_url
        inner_grid = NextComicsInnerGrid(id='inner_grid'+str(prev_comic.comic_id_number))
        comic_thumb = NextComicImage(source=self.prev_comic.thumb_url,id=str(prev_comic.comic_id_number),nocache=True)

        comic_thumb.comic = self.prev_comic
        comic_thumb.comics_collection = self.comics_collection
        inner_grid.add_widget(comic_thumb)

        smbutton = NextComicsPagebntlbl(text=comic_name)
        inner_grid.add_widget(smbutton)
        content = inner_grid


        self.prev_dialog = Dialog(title="Load Next",
                             content=content,
                             size_hint=(.3, .3),
                             height=dp(250),
                             auto_dismiss=True)
        comic_thumb.bind(on_release=self.prev_dialog.dismiss)
        comic_thumb.bind(on_release=comic_thumb.click)

    def open_prev_dialog(self):
         self.prev_dialog.open()

    def load_next_comic(self):
        self.dialog.dismiss()
        self.load_comic(self.next_comic,self.comics_collection)

    def load_prev_comic(self):
        self.dialog.dismiss()
        self.load_comic(self.prev_comic,self.comics_collection)



    def get_prev_comic(self):
        comics_collection = self.comics_collection.comics
        comic = self.comic
        index = comics_collection.index(comic) # first index where x appears
        if index < len(comics_collection):
            if index == 0:
                prev_comic = comics_collection[index]
            else:
                prev_comic = comics_collection[index-1]
        return prev_comic

class ComicCarousel(Carousel):
    # comic_image_src = StringProperty()
    pass
class ComicFloatLayout(FloatLayout):
    pass

class ComicPageScatter(ScatterLayout):
    def __init__(self, **kwargs):
        super(ComicPageScatter, self).__init__(**kwargs)
        self.zoom_state = 'normal'
        self.move_state = 'open'

    def open_mag_glass(self):
        Logger.debug('my id=%s' % str(self.id))

        mag_glass_setting_x = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        mag_glass_setting_y = int(App.get_running_app().config.get('Display', 'mag_glass_size'))

        comic_image_id = self.id.replace('comic_scatter','pi_')
        print App.get_running_app().root.ids
        try:
            for child in self.walk():
                print child.id
                if child.id == comic_image_id:
                    image_w = child
                    Logger.debug('>>>>>Found grandchild named %s this is the image' %comic_image_id)
                elif child.id == 'mag_glass':
                    mag_glass_w = child
        except:
           Logger.critical('Some bad happened in _call_mag')
        else:
            print 'image_w = %s' % str(image_w)
            if self.move_state == 'open':
                self.move_state = 'locked'
                self.do_scale=False
                self.do_translation=False
                Logger.debug('image_w.center = %d,%d' % (image_w.center_x,image_w.center_y))

                mag_glass = MagnifyingGlassScatter(
                                                        do_rotation=False, do_scale=False,
                                                        pos=((image_w.center_x-(mag_glass_setting_x)),
                                                             (image_w.center_y-(mag_glass_setting_y))
                                                         ),id='mag_glass'
                                                  )
                mag_glass.page_widget = image_w
                mag_glass_image = Image(size_hint= (None,None),pos_hint={'x':1, 'y':1},id='mag_image',keep_ratio=True,
                                        allow_stretch=False,size=mag_glass.size )
                mag_glass.mag_img = mag_glass_image
                mag_glass_image.texture = image_w.texture.get_region(
                                            mag_glass.x,mag_glass.y,mag_glass_setting_x,mag_glass_setting_y)
                mag_glass.add_widget(mag_glass_image)
                self.add_widget(mag_glass)
                print mag_glass.scale
                mat = Matrix().scale(2, 2, 2)
                mag_glass.apply_transform(mat)
            else:
                self.move_state = 'open'
                self.do_scale=True
                self.do_translation=True

                self.remove_widget(mag_glass_w)

    def on_touch_down(self, touch):
        if touch.is_double_tap:
            if self.zoom_state == 'zoomed':
                self.zoom_state = 'normal'
                mat = self.transform_inv
                self.apply_transform(mat,anchor=(0,0))
            elif self.zoom_state == 'normal':
                self.zoom_state = 'zoomed'
                mat = Matrix().scale(2,2,2)
                self.apply_transform(mat,anchor=touch.pos)
        return super(ComicPageScatter, self).on_touch_down(touch)

    def on_transform_with_touch(self,touch):
         self.zoom_state = 'zoomed'
         return super(ComicPageScatter, self).on_transform_with_touch(touch)

class ComicPageImage(AsyncImage):
    parent_id = StringProperty()
    nocache=False
    def __init__(self, **kwargs):
       # self.page_tb_inrgrid =ThumbPopPageInnerGrid(id=str(self._index))
        super(ComicPageImage, self).__init__(**kwargs)
        self._index = kwargs.pop('_index',0)
        self._thumb = Image()

    def _new_image_downloaded(self, scatter , outer_grid,comic_number, proxyImage,):
        '''Fired once the image is downloaded and ready to use'''
        def _remove_widget():
            carousel.remove_widget(scatter)

        def _add_parts():
            part_1 = ComicPageImage(_index=self._index,id='pi_'+str(self._index)+'b')
            part_2 = ComicPageImage(_index=self._index+1,id='pi_'+str(self._index)+'b')
            scatter_1 = ComicPageScatter(id='comic_scatter'+str(self._index))
            scatter_2 = ComicPageScatter(id='comic_scatter'+str(self._index)+'b')
            part_1.texture = proxyImage.image.texture.get_region(0,0,c_width/2,c_height)
            part_2.texture = proxyImage.image.texture.get_region((c_width/2+1),0,c_width/2,c_height)
            scatter_1.add_widget(part_1)
            scatter_2.add_widget(part_2)
            carousel.add_widget(scatter_1,i)
            carousel.add_widget(scatter_2,i+1)
        def _add_thumbs():
            carousel.remove_widget(scatter)
            part_1 = ComicPageImage(_index=self._index,id='pi_'+str(self._index)+'b')
            part_2 = ComicPageImage(_index=self._index+1,id='pi_'+str(self._index)+'b')
            scatter_1 = ComicPageScatter(id='comic_scatter'+str(self._index))
            scatter_2 = ComicPageScatter(id='comic_scatter'+str(self._index)+'b')
            part_1.texture = proxyImage.image.texture.get_region(0,0,c_width/2,c_height)
            part_2.texture = proxyImage.image.texture.get_region((c_width/2+1),0,c_width/2,c_height)
            scatter_1.add_widget(part_1)
            scatter_2.add_widget(part_2)
            carousel.add_widget(scatter_1,i)
            carousel.add_widget(scatter_2,i+1)
            #redo page thumb to have both parts
            inner_grid_1 = ThumbPopPageInnerGrid(id='inner_grid'+str(self._index))
            part1_thumb = ThumbPopPageImage(id=scatter_1.id,_index=self._index)
            inner_grid_1.add_widget(part1_thumb)
            part1_thumb.bind(on_release=part1_thumb.click)
            smbutton_1 = ThumbPopPagebntlbl(text='P%sa'%str(self._index+1))
            inner_grid_1.add_widget(smbutton_1)
            outer_grid.add_widget(inner_grid_1)

            inner_grid_2 = ThumbPopPageInnerGrid(id='inner_grid'+str(self._index+1))
            part2_thumb = ThumbPopPageImage(id=scatter_2.id,_index=self._index+1)
            inner_grid_2.add_widget(part2_thumb)
            part2_thumb.bind(on_release=part2_thumb.click)
            smbutton_2 = ThumbPopPagebntlbl(text='P%sb'%str(self._index+1))
            inner_grid_2.add_widget(smbutton_2)
            outer_grid.add_widget(inner_grid_2)


        if proxyImage.image.texture:
            split_dbl_page = App.get_running_app().config.get('Display', 'dblpagesplit')
            if proxyImage.image.texture.width > 2*Window.width and split_dbl_page == '1':

                base_url = App.get_running_app().config.get('Server', 'url')
                src_thumb = "%s/comic/%d/page/%d?max_height=200#.jpg" % (base_url, comic_number, self._index)
                app = App.get_running_app()
                inner_grid_id ='inner_grid' + str(self._index)
                page_image_id = str(self._index)
                carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
                inner_grid_id = 'inner_grid%s'%str(self._index)
                c_width = self.texture.width
                c_height = self.texture.height
                Logger.debug('<<<New Split it running>>>>')
                i = 0
                for slide in carousel.slides:
                    if slide.id == scatter.id:
                        _remove_widget()
                        _add_parts()
                    i+=1
                for thumb in outer_grid.walk():
                    if thumb.id == 'inner_grid_id':
                        outer_grid.remove_widet(thumb)
                        _add_thumbs()
            else:
                if proxyImage.image.texture.width > 2*Window.width:
                    scatter.size_hint=(2,1)

                    #self.size_hint=(2,1)

    def _abort_download(self, dt):
        '''Stop the image from downloading'''
        Loader.stop()








#<<<<Following are class for popup at bottom page for pressing and going to page x
class ThumbPopPagePopup(Popup):
    pass

class ThumbPopPageScroll(ScrollView):
    pass

class ThumbPopPageOutterGrid(GridLayout):
    pass

class ThumbPopPageInnerGrid(GridLayout):
    pass

class ThumbPopPagebntlbl(Button):
    pass

class ThumbPopPageSmallButton(Button):
    pass

class ThumbPopPageImage(RectangularRippleBehavior,ButtonBehavior,AsyncImage):

    def click(self,instance):
        app = App.get_running_app()
        app.root.current = 'comic_screen'
        thum_pop = app.root.ids['comic_screen_id'].thumb_pop
        thum_pop.dismiss()
        carousel = App.get_running_app().root.ids['comic_screen_id'].ids['comic_carousel']
        for slide in carousel.slides:
            if slide.id == self.id:
                use_slide = slide
        carousel.load_slide(use_slide)
#<<<<<<<<<<


#<<<<Following are class for Next list>>>>>>>>>
class NextComicsScroll(ScrollView):
    pass

class NextComicsOuterGrid(GridLayout):
    pass

class NextComicsInnerGrid(GridLayout):
    pass

class NextComicsPagebntlbl(Label):
    pass

class NextComicImage(RectangularRippleBehavior,ButtonBehavior,AsyncImage):

    comic = ObjectProperty()
    comics_collection = ObjectProperty()



    def enable_me(self,instance):
        self.disabled = False

    def click(self,instance):
        self.disabled = True
        app = App.get_running_app()
        comic_screen = app.root.get_screen('comic_screen')
        print 'comic id = %d'%self.comic.comic_id_number
        comic_screen.load_comic(self.comic,self.comics_collection)
        Clock.schedule_once(self.enable_me, .5)
#<<<<<<<<<<

class ControlButton(Button):
    def enable_me(self,instance):
        Logger.debug('I am enabled')
        self.disabled = False

class MagnifyingGlassScatter(Scatter):
    def __init__(self,**kwargs):
        super(MagnifyingGlassScatter, self).__init__(**kwargs)
        self.mag_glass_x = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        self.mag_glass_y = int(App.get_running_app().config.get('Display', 'mag_glass_size'))
        self.page_widget = ''
        self.mag_img = ''

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            # do whatever else here
        return super(MagnifyingGlassScatter, self).on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            print 'touch = %s'%str(touch.pos)
            print 'image = %s'%str(self.page_widget.size)
            #get the middle of mag glass
            my_x = self.x
            m_y = self.y
            #self.mag_img.texture = self.page_widget.texture.get_region(my_x,m_y,my_x,my_y)
            self.mag_img.texture = self.page_widget.texture.get_region(my_x,m_y,self.mag_glass_x/2,self.mag_glass_y/2)
            # now we only handle moves which we have grabbed

        return super(MagnifyingGlassScatter, self).on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
        return super(MagnifyingGlassScatter, self).on_touch_up(touch)
            # and finish up here

class RippleButton(RectangularRippleBehavior,Button):
    pass