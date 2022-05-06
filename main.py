import datetime

import shutil



from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.animation import Animation
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
import random
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar

import plyer
from kivymd.utils.fitimage import FitImage
from plyer import filechooser
from GoogleNews import GoogleNews
import pandas as pd

import os
from icrawler.builtin import GoogleImageCrawler
import threading
import mysql.connector

import send_email
from kivy.graphics.texture import Texture
import cv2
from kivy.uix.image import Image
import Cam




class NavigationWindow(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)







class CustomSnackbar(Snackbar):
    icon = StringProperty(None)


class MainLayout(Widget):
    path = ''
    imagen = ''
    miky = 1

    ortiz = 50
    photos = ['forest_1.jpg', 'forest_2.jpg', 'forest_3.jpg', 'forest_4.jpg', 'forest_5.jpg', 'forest_6.jpg',
              'forest_7.jpg', 'forest_8.jpg', 'forest_9.jpg']
    random.shuffle(photos)

    file_name_title = []
    folder_name = 'news'
    title_news = []
    topic_name = 'USA'
    topic_photo = []
    countries = ['New 1', 'New 2', 'New 3', 'New 4', 'New 5', 'New 6', 'New 7', 'New 8', 'New 9', 'New  10']

    index = 0

    cam_on_off = False

    changer_cam = ''
    capture = cv2.VideoCapture(0)
    image_path = ''
    C = ''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.background.img = self.photos[random.randint(0, 8)]
        #self.ids.select_coun.values = self.countryList
        time_year = datetime.datetime.now()




        User = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='mikyortiz1224@',
            database='second_database'

        )

        c = User.cursor()

        # check for

        c.execute(
            'SELECT * FROM User_Registration')

        record = c.fetchall()

        print(record)

        miky = []
        for i in range(1950, time_year.year+1):
            miky.append(f"{i}")
        miky.reverse()

        self.ids.User_year_birth.values = miky

        for i in range(1,32):
            self.ids.User_day_birth.values.append(f"{i}")

        self.image = Image(size_hint=(None, None), width='600dp', height='350dp', pos_hint={'center_y':0.65, 'center_x': 0.5})

        self.ids.MDF.add_widget(self.image)
        self.capture = cv2.VideoCapture(0)
        self.image.source = 'cam_off.png'

        pp = threading.Thread(target=self.load_video(None))
        pp.start()



    def on_kv_post(self, base_widget):
        Clock.schedule_interval(self.texting, 1)
        Clock.schedule_interval(self.bu, 0.1)
        Clock.schedule_interval(self.load_video, 0.1 / 60.0)
        Clock.schedule_interval(self.video_layout, 0.1 / 60.0)




    def save_image_edited(self):


        if len(self.ids.name_photo.text) == 0:
            CustomSnackbar(text='Image saved', icon='alert-circle-outline', snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.4, bg_color=(149 / 255, 33 / 255, 255 / 255, 0.5)).open()

        elif len(self.ids.name_photo.text) != 0:

            print(self.ids.format_img.text)

            if self.name == "Blue_light":
                cv2.imwrite(f'C:/Users/Mikyo/OneDrive/Escritorio/{self.ids.name_photo.text}.{self.ids.format_img.text}', self.blue_light[0])

            elif self.name == "comic_Uncolored":
                cv2.imwrite(f'C:/Users/Mikyo/OneDrive/Escritorio/{self.ids.name_photo.text}.{self.ids.format_img.text}', self.comic_uncolored[0])


            elif self.name == 'Comic':
                cv2.imwrite(f'C:/Users/Mikyo/OneDrive/Escritorio/{self.ids.name_photo.text}.{self.ids.format_img.text}', self.comic[0])


            elif self.name == 'Canny':
                cv2.imwrite(f'C:/Users/Mikyo/OneDrive/Escritorio/{self.ids.name_photo.text}.{self.ids.format_img.text}', self.self.canny[0])


            elif self.name == 'thresh':
                cv2.imwrite(f'C:/Users/Mikyo/OneDrive/Escritorio/{self.ids.name_photo.text}.{self.ids.format_img.text}', self.thresh[0])

            CustomSnackbar(text='Image saved', icon='content-save-edit',snackbar_x="10dp",
                               snackbar_y="10dp",
                               size_hint_x=.4, bg_color=(149/255,33/255,255/255,0.5)).open()
            self.ids.name_photo.text = ''
            self.ids.format_img.text = 'png'
            self.ids.second_screen.current = 'load_img'


    def upload_image(self, name):

        self.name = name


        if self.name == "Blue_light":
            self.ids.img_edit.texture = self.texture_blue_light

        elif self.name == "comic_Uncolored":
            self.ids.img_edit.texture = self.texture_comic_uncolored

        elif self.name == 'Comic':
            self.ids.img_edit.texture = self.texture_comic

        elif self.name == 'Canny':
            self.ids.img_edit.texture =self.tecture_canny

        elif self.name == 'thresh':
            self.ids.img_edit.texture = self.texture_thresh

    def load_img_front(self):

        

        try:


            function = Cam.Image_Mode()

            #load cany image
            C = cv2.imread(self.image_path)
            self.canny = function.img_canny(C)

            buffer = bytes(cv2.flip(self.canny[0], 0))
            texture = Texture.create(size=(self.canny[0].shape[1], self.canny[0].shape[0]), colorfmt=self.canny[1])
            texture.blit_buffer(buffer, colorfmt=self.canny[1], bufferfmt='ubyte')
            self.ids.img_canny_pic.texture = texture
            self.tecture_canny = texture



            #load thread image
            T = cv2.imread(self.image_path)
            self.thresh = function.img_thresh(T)

            buffer_thresh = bytes(cv2.flip(self.thresh[0], 0))
            texture_thresh = Texture.create(size=(self.thresh[0].shape[1], self.thresh[0].shape[0]), colorfmt=self.thresh[1])
            texture_thresh.blit_buffer(buffer_thresh, colorfmt=self.thresh[1], bufferfmt='ubyte')
            self.ids.img_thresh_pic.texture = texture_thresh
            self.texture_thresh = texture_thresh



            #load comic image
            CO = cv2.imread(self.image_path)
            self.comic = function.comic(CO)

            buffer_comic = bytes(cv2.flip(self.comic[0], 0))

            texture_comic = Texture.create(size=(self.comic[0].shape[1], self.comic[0].shape[0]), colorfmt=self.comic[1])
            texture_comic.blit_buffer( buffer_comic, colorfmt=self.comic[1], bufferfmt='ubyte')

            self.ids.img_comic_pic.texture = texture_comic
            self.texture_comic = texture_comic


            #load comic uncolored

            COU = cv2.imread(self.image_path)
            self.comic_uncolored = function.comic_uncolored(COU)

            buffer_comic_uncolored = bytes(cv2.flip(self.comic_uncolored[0], 0))

            texture_comic_uncolored = Texture.create(size=(self.comic_uncolored[0].shape[1], self.comic_uncolored[0].shape[0]), colorfmt=self.comic_uncolored[1])
            texture_comic_uncolored.blit_buffer(buffer_comic_uncolored, colorfmt=self.comic_uncolored[1], bufferfmt='ubyte')

            self.ids.img_comic_uncolored_pic.texture = texture_comic_uncolored
            self.texture_comic_uncolored = texture_comic_uncolored


            #load blue_light

            BL = cv2.imread(self.image_path)
            self.blue_light = function.blue_light(BL)

            buffer_blue_light = bytes(cv2.flip(self.blue_light[0], 0))

            texture_blue_light = Texture.create(size=(self.blue_light[0].shape[1], self.blue_light[0].shape[0]), colorfmt=self.blue_light[1])
            texture_blue_light.blit_buffer(buffer_blue_light, colorfmt=self.blue_light[1], bufferfmt='ubyte')


            self.ids.img_blue_light_pic.texture = texture_blue_light
            self.texture_blue_light = texture_blue_light

        except:
            print("error")






    def video_layout(self,frame):
        if self.cam_on_off is False:
            pass


        elif self.cam_on_off is True:
            #Canny plus real

            canny_layout = Cam.Cam_Mode.canny(self, self.video_frame_layout)
            buffer_canny_layout = bytes(cv2.flip(canny_layout[0], 0))

            texture_canny_layout = Texture.create(size=(canny_layout[0].shape[1], canny_layout[0].shape[0]), colorfmt=canny_layout[1])
            texture_canny_layout.blit_buffer(buffer_canny_layout, colorfmt=canny_layout[1], bufferfmt='ubyte')
            self.ids.video_canny_cam.texture = texture_canny_layout

            #lauout kernel
            kernel_layout = Cam.Cam_Mode.kernel(self, self.video_frame_layout)
            buffer_kernel_layout = bytes(cv2.flip(kernel_layout[0], 0))

            texture_kernel_layout = Texture.create(size=(kernel_layout[0].shape[1], kernel_layout[0].shape[0]), colorfmt=kernel_layout[1])
            texture_kernel_layout.blit_buffer(buffer_kernel_layout, colorfmt=kernel_layout[1],bufferfmt='ubyte')

            self.ids.video_Kernel_cam.texture = texture_kernel_layout

            #kernal_light layout
            kernal_light_layout = Cam.Cam_Mode.kernal_light(self, self.video_frame_layout)
            buffer_kernal_light_layout = bytes(cv2.flip(kernal_light_layout[0], 0))

            texture_kernal_light_layout = Texture.create(size=(kernal_light_layout[0].shape[1], kernal_light_layout[0].shape[0]), colorfmt=kernal_light_layout[1])
            texture_kernal_light_layout.blit_buffer(buffer_kernal_light_layout, colorfmt=kernal_light_layout[1],bufferfmt='ubyte' )

            self.ids.video_Kernel_Light_cam.texture = texture_kernal_light_layout


            #video_replicate_cam layout
            replicate_layout = Cam.Cam_Mode.replicate(self, self.video_frame_layout)
            buffer_replicate_layout = bytes(cv2.flip(replicate_layout[0], 0))

            texture_replicate_layout = Texture.create(size=(replicate_layout[0].shape[1], replicate_layout[0].shape[0]), colorfmt=replicate_layout[1])
            texture_replicate_layout.blit_buffer(buffer_replicate_layout, colorfmt=replicate_layout[1], bufferfmt='ubyte')

            self.ids.video_replicate_cam.texture = texture_replicate_layout

            #reflect layout
            reflect_layout = Cam.Cam_Mode.reflect(self, self.video_frame_layout)
            buffer_reflect_layout = bytes(cv2.flip(reflect_layout[0], 0))

            texture_reflect_layout = Texture.create(size=(reflect_layout[0].shape[1], reflect_layout[0].shape[0]), colorfmt=reflect_layout[1])
            texture_reflect_layout.blit_buffer(buffer_reflect_layout, colorfmt=reflect_layout[1], bufferfmt='ubyte' )

            self.ids.video_reflect_cam.texture = texture_reflect_layout

            #reflect101 layout

            reflect101_layout = Cam.Cam_Mode.reflect101(self, self.video_frame_layout)
            buffer_reflect101_layout = bytes(cv2.flip(reflect101_layout[0], 0))

            texture_reflect101_layout = Texture.create(size=(reflect101_layout[0].shape[1], reflect101_layout[0].shape[0]), colorfmt=reflect101_layout[1])
            texture_reflect101_layout.blit_buffer(buffer_reflect101_layout, colorfmt=reflect101_layout[1], bufferfmt='ubyte')

            self.ids.video_reflect101_cam.texture = texture_reflect101_layout

            #wrap layout
            wrap_layout = Cam.Cam_Mode.wrap(self, self.video_frame_layout)
            buffer_wrap_layout = bytes(cv2.flip(wrap_layout[0], 0))

            texture_wrap_layout = Texture.create(size=(wrap_layout[0].shape[1], wrap_layout[0].shape[0]), colorfmt=wrap_layout[1])
            texture_wrap_layout.blit_buffer(buffer_wrap_layout, colorfmt=wrap_layout[1], bufferfmt='ubyte')

            self.ids.video_wrap_cam.texture = texture_wrap_layout

            #constant layout

            constant_layout = Cam.Cam_Mode.constant(self, self.video_frame_layout)
            buffer_constant_layout = bytes(cv2.flip(constant_layout[0], 0))

            texture_constant_layout = Texture.create(size=(constant_layout[0].shape[1], constant_layout[0].shape[0]), colorfmt=constant_layout[1])
            texture_constant_layout.blit_buffer(buffer_constant_layout, colorfmt=constant_layout[1], bufferfmt='ubyte')

            self.ids.video_constant_cam.texture = texture_constant_layout

            # thresh layout

            layout_thresh = Cam.Cam_Mode.frame_thresh(self, self.video_frame_layout)
            buffer_layout_thresh = bytes(cv2.flip(layout_thresh[0], 0))

            texture_layout_thresh = Texture.create(size=(layout_thresh[0].shape[1], layout_thresh[0].shape[0]),
                                                     colorfmt=layout_thresh[1])
            texture_layout_thresh.blit_buffer(buffer_layout_thresh, colorfmt=layout_thresh[1], bufferfmt='ubyte')

            self.ids.frame_thresh_video.texture = texture_layout_thresh

            # comic_uncolored layout

            layout_comic_uncolored = Cam.Cam_Mode.comic_uncolored_frame(self, self.video_frame_layout)
            buffer_comic_uncolored = bytes(cv2.flip(layout_comic_uncolored[0], 0))

            texture_comic_uncolored = Texture.create(size=(layout_comic_uncolored[0].shape[1], layout_comic_uncolored[0].shape[0]),
                                                   colorfmt=layout_comic_uncolored[1])
            texture_comic_uncolored.blit_buffer(buffer_comic_uncolored, colorfmt=layout_comic_uncolored[1], bufferfmt='ubyte')

            self.ids.comic_uncolored_video.texture = texture_comic_uncolored

            # blue_light layout

            layout_blue_light = Cam.Cam_Mode.blue_light_frame(self, self.video_frame_layout)
            buffer_blue_light = bytes(cv2.flip(layout_blue_light[0], 0))

            texture_blue_light = Texture.create(
                size=(layout_blue_light[0].shape[1], layout_blue_light[0].shape[0]),
                colorfmt=layout_blue_light[1])
            texture_blue_light.blit_buffer(buffer_blue_light, colorfmt=layout_blue_light[1],
                                                bufferfmt='ubyte')

            self.ids.blue_light_video.texture = texture_blue_light



    def load_video(self,k):

        if self.cam_on_off is False:
            pass


        elif self.cam_on_off is True:


            ret, frame = self.capture.read()
            # frame initialize
            self.image_frame = frame
            self.video_frame_layout = frame
            color= 'bgr'
            if self.changer_cam == 'Canny':
                canny_change = Cam.Cam_Mode.canny(self, frame)
                frame = canny_change[0]
                self.image_frame = frame
                color = canny_change[1]

            elif self.changer_cam == 'blue_light':
                blue_light = Cam.Cam_Mode.blue_light_frame(self, frame)
                frame = blue_light[0]
                self.image_frame = frame
                color = blue_light[1]

            elif self.changer_cam == 'comic_uncolored':
                comic_uncolored = Cam.Cam_Mode.comic_uncolored_frame(self, frame)
                frame = comic_uncolored[0]
                self.image_frame = frame
                color = comic_uncolored[1]

            elif self.changer_cam == 'frame_thresh':
                thresh = Cam.Cam_Mode.frame_thresh(self, frame)
                frame = thresh[0]
                self.image_frame = frame
                color = thresh[1]


            elif self.changer_cam == 'Kernel':
                kernel_change = Cam.Cam_Mode.kernel(self, frame)
                frame = kernel_change[0]
                self.image_frame = frame
                color = kernel_change[1]


            elif self.changer_cam == 'Kernel_Light':
                change_light = Cam.Cam_Mode.kernal_light(self, frame)
                frame = change_light[0]
                self.image_frame = frame
                color = change_light[1]

            elif self.changer_cam == 'Replicate':
                Replicate = Cam.Cam_Mode.replicate(self,frame)
                frame = Replicate[0]
                self.image_frame = frame
                color = Replicate[1]


            elif self.changer_cam == 'Reflect':
                Reflect = Cam.Cam_Mode.reflect(self,frame)
                frame = Reflect[0]
                self.image_frame = frame
                color = Reflect[1]
            elif self.changer_cam == 'Reflect101':
                Reflect101 = Cam.Cam_Mode.reflect101(self, frame)
                frame = Reflect101[0]
                self.image_frame = frame
                color = Reflect101[1]

            elif self.changer_cam == 'Wrap':
                wrap = Cam.Cam_Mode.wrap(self, frame)
                frame = wrap[0]
                self.image_frame = frame
                color = wrap[1]

            elif self.changer_cam == 'Constant':
                Constant = Cam.Cam_Mode.constant(self, frame)
                frame = Constant[0]
                self.image_frame = frame
                color = Constant[1]

            elif self.changer_cam =='Default':
                pass

            buffer = bytes(cv2.flip(frame, 0))

            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt=color)
            texture.blit_buffer(buffer, colorfmt=color, bufferfmt='ubyte')

            self.image.texture = texture



    def Cam_Model(self,value):

        if self.cam_on_off is False:
            pass

        elif self.cam_on_off is True:

            self.changer_cam = value



    def cam_button(self):

        if self.cam_on_off is False:
            self.cam_on_off = True

            self.ids.toolbar_cam.right_action_items = [['camera-off', lambda x: self.cam_button()],
                                                       ['close-circle', lambda x: self.Cam_Model('Default')],
                                                       ['content-save', lambda x: self.save_picture()]]



        elif self.cam_on_off is True:

            self.cam_on_off = False
            self.ids.toolbar_cam.right_action_items = [['camera', lambda x: self.cam_button()],
                                                       ['close-circle', lambda x: self.Cam_Model('Default')],
                                                       ['content-save', lambda x: self.save_picture()]]



    def navi_screen(self, value):


        if value == 'image':
            self.ids.toolbar_cam.right_action_items = [['baseball'],
                                                       ['account-arrow-down'],
                                                       ['air-conditioner']]


            if self.cam_on_off is True:
                self.cam_on_off = False
        elif value == 'video':
            self.ids.toolbar_cam.right_action_items = [['camera', lambda x: self.cam_button()],
                                                       ['close-circle', lambda x: self.Cam_Model('Default')],
                                                       ['content-save', lambda x: self.save_picture()]]






    def save_picture(self):


        if self.cam_on_off is True:
            import os
            miky = random.randint(0, 9999999)

            image_saced = f'C:/Users/Mikyo/OneDrive/Escritorio/Picture-{miky}.png'

            cv2.imwrite(image_saced, self.image_frame)
            CustomSnackbar(text='[color=#000000]Image Saved[/color]', icon=image_saced,
                           snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.4, bg_color=(149/255,33/255,255/255,0.5)).open()

            cam_anim = Animation(opacity=0.5, duration=0.01)

            cam_anim += Animation(opacity=1, duration=0.01)

            cam_anim.start(self.ids.Cam_AI)


            self.img_anim = FitImage(size_hint=(0.3, 0.35), pos_hint={'center_y': 0.65, 'center_x': 0.5})

            self.img_anim.source = image_saced

            self.ids.MDF.add_widget(self.img_anim)

            anim = Animation(size_hint=(0.2, 0.3),
                             pos_hint={'center_y': 0.2, 'center_x': 0.8}, radius=[20,20,20,20], duration=0.8)

            anim += Animation(duration=2)

            anim += Animation(size_hint=(0.25, 0.35), duration=0.5)

            anim += Animation(size_hint=(0, 0), duration=0.5)

            anim.start(self.img_anim)


        else:
            pass




    counter = 0
    COUN = 0
    pasa_n = False



    opac = 0

    ram = 0

    swiper_count = 0

    swiper_accumulator = 0

    def swipe_right(self):
        self.swiper_accumulator += 1
        self.swiper_count = 0

    def swipe_left(self):
        self.swiper_accumulator -= 1
        self.swiper_count = 0

    news_status = ""
    def news(self):
        self.news_status = "Processing"
        Clock.schedule_once(self.timing)

        print(self.news_status)

        news = GoogleNews(period='1d')
        news.search(self.topic_name)
        result = news.result()
        data = pd.DataFrame.from_dict(result)
        data.head()



        for i in result:

            self.title_news.append(i['title'])

        try:


            self.topic_photo = self.title_news
            # print("title array", self.topic_photo)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[0]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[0]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[1]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[1]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[2]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[2]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[3]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[3]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[4]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[4]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[5]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[5]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[6]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[6]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[7]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[7]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[8]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[8]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[9]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[9]}',
                                      max_num=1)

        except:
            self.topic_photo = self.title_news
            # print("title array", self.topic_photo)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[0]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[0]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[1]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[1]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[2]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[2]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[3]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[3]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[4]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[4]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[5]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[5]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[6]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[6]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[7]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[7]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[8]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[8]}',
                                      max_num=1)

            self.google_crawler = GoogleImageCrawler(storage={'root_dir': f"{self.countries[9]}"})
            self.google_crawler.crawl(keyword=f'{self.topic_photo[9]}',
                                      max_num=1)

        for i in range(len(self.countries)):
            for dirpath, dirname, filename in os.walk(self.countries[i]):
                # print("dirpath", dirpath)
                # print("dirname", dirname)
                # print("filename", filename)
                self.file_name_title.append(filename)

        try:
            self.ids.image_back_1.source = f'{self.countries[0]}/{self.file_name_title[0][0]}'
            self.ids.title_1.text = f'{self.title_news[0]}'
        except:
            self.ids.image_back_1.source = f'reflect.png'
            self.ids.title_1.text = f'{self.title_news[0]}'


        try:

            self.ids.image_back_2.source = f'{self.countries[1]}/{self.file_name_title[1][0]}'
            self.ids.title_2.text = f'{self.title_news[1]}'
        except:
            self.ids.image_back_2.source = f'reflect.png'
            self.ids.title_2.text = f'{self.title_news[1]}'

        try:
            self.ids.image_back_3.source = f'{self.countries[2]}/{self.file_name_title[2][0]}'
            self.ids.title_3.text = f'{self.title_news[2]}'
        except:
            self.ids.image_back_3.source = f'reflect.png'
            self.ids.title_3.text = f'{self.title_news[2]}'

        try:

            self.ids.image_back_4.source = f'{self.countries[3]}/{self.file_name_title[3][0]}'
            self.ids.title_4.text = f'{self.title_news[3]}'
        except:
            self.ids.image_back_4.source = f'reflect.png'
            self.ids.title_4.text = f'{self.title_news[3]}'

        try:

            self.ids.image_back_5.source = f'{self.countries[4]}/{self.file_name_title[4][0]}'
            self.ids.title_5.text = f'{self.title_news[4]}'
        except:
            self.ids.image_back_5.source = f'reflect.png'
            self.ids.title_5.text = f'{self.title_news[4]}'


        try:
            self.ids.image_back_6.source = f'{self.countries[5]}/{self.file_name_title[5][0]}'
            self.ids.title_6.text = f'{self.title_news[5]}'
        except:
            self.ids.image_back_6.source = f'res.png'
            self.ids.title_6.text = f'{self.title_news[5]}'


        try:
            self.ids.image_back_7.source = f'{self.countries[6]}/{self.file_name_title[6][0]}'
            self.ids.title_7.text = f'{self.title_news[6]}'
        except:
            self.ids.image_back_7.source = f'res.png'
            self.ids.title_7.text = f'{self.title_news[6]}'

        try:
            self.ids.image_back_8.source = f'{self.countries[7]}/{self.file_name_title[7][0]}'
            self.ids.title_8.text = f'{self.title_news[7]}'
        except:
            self.ids.image_back_8.source = f'res.png'
            self.ids.title_8.text = f'{self.title_news[7]}'

        try:
            self.ids.image_back_9.source = f'{self.countries[8]}/{self.file_name_title[8][0]}'
            self.ids.title_9.text = f'{self.title_news[8]}'
        except:
            self.ids.image_back_9.source = f'res.png'
            self.ids.title_9.text = f'{self.title_news[8]}'

        try:
            self.ids.image_back_10.source = f'{self.countries[9]}/{self.file_name_title[9][0]}'
            self.ids.title_10.text = f'{self.title_news[9]}'
        except:
            self.ids.image_back_10.source = f'res.png'
            self.ids.title_10.text = f'{self.title_news[9]}'


        self.news_status = "done"
        Clock.schedule_once(self.timing)
        print(self.news_status)


    def texting(self, k):



        if self.ids.screen_manager.current == "Camera AI":
            pass
        else:

            if self.cam_on_off is True:
                self.cam_on_off = False

            pass
        try:

            if self.swiper_accumulator == len(self.ids.swiper.get_items()):
                self.swiper_accumulator = 0

            if self.swiper_count == len(self.ids.swiper.get_items()):
                self.swiper_count = 0

                self.swiper_accumulator += 1
                self.ids.swiper.set_current(self.swiper_accumulator)

            self.swiper_count += 1
        except:
            self.swiper_accumulator = 0
            self.ids.swiper.set_current(self.swiper_accumulator)

        self.COUN += 1
        # print(self.COUN)

        if self.COUN == 10:

            # print("minus")
            self.miky -= 1
            # print(self.miky)

            anim = Animation(opacity=self.miky)

            anim += Animation(opacity=1)

            anim.start(self.ids.background)

            self.COUN = 0

        elif self.miky == 0:
            self.miky = 1
            # print("changed")

            # print(self.ram, "photo number")
            if self.ram == len(self.photos):
                self.ram = 0

            self.ids.background.img = self.photos[self.ram]

            self.ram += 1

    def closed(self, ins):

        return self.dialog.dismiss()

    def show_alert_dialog(self):

        self.dialog = MDDialog(
            text="Testing Dialog", radius=[20, 7, 20, 7], title="Miky App",
            type="custom",

            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=(22 / 255, 0 / 255, 0 / 255, 1), on_press=self.closed
                ),
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=(22 / 255, 0 / 255, 0 / 255, 1),
                    on_press=self.closed
                ),
            ],

        )
        self.dialog.open()



    def selection(self, path):

        try:

            path_str = str(path[0])
            #Snackbar(text=path_str).open()
            car = 0

            for i in path_str:

                if i == path_str[2]:
                    path_str = path_str.replace(f'{i}', '/')
                car += 1

            self.image_path = path_str
            #self.ids.img_edit.source = f'{path_str}'

            default = cv2.imread(f'{self.image_path}')


            buffer_default = bytes(cv2.flip(default, 0))

            texture_default = Texture.create(size=(default.shape[1], default.shape[0]), colorfmt='bgr')
            texture_default.blit_buffer(buffer_default, colorfmt='bgr', bufferfmt='ubyte')

            self.ids.img_edit.texture = texture_default

            self.ids.second_screen.current = 'save_img'

            self.image_path=''

        except:
            print("error")

    def file_manager_open(self):

        try:

            self.path = filechooser.open_file(on_selection=self.selection)

        except:
            print("error")

    def bu(self, k):
        if self.ids.login_anim.opacity == 0:

            self.anim_active = True
        else:

            self.anim_active = False

    anim_active = True

    def Login_User(self):

        for i in self.ids.Username.text:
            if " " == i:
                self.ids.Username.text = self.ids.Username.text.replace(i, "")



        if len(self.ids.Password.text) == 0 or len(self.ids.Username.text) == 0:

            CustomSnackbar(text="Missing Username or missing the password",snackbar_x="10dp",
    snackbar_y="10dp",
    size_hint_x=.9, bg_color=(250/255,5/255,25/255, 1), icon="information"

            ).open()


        else:




            User = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='mikyortiz1224@',
                database='second_database'

            )

            c = User.cursor()


            #check for

            c.execute(
                'SELECT * FROM User_Registration WHERE name =' + f'"{self.ids.Username.text}"' + 'AND' + ' password =' + f'"{self.ids.Password.text}"')

            record = c.fetchall()

            print(record)


            try:

                if self.ids.Username.text in record[0] or self.ids.Password.text in record[0]:

                    self.TH = threading.Thread(target=self.news)
                    self.TH.start()

                    CustomSnackbar(text="logged in", snackbar_x="10dp",
    snackbar_y="10dp",
    size_hint_x=.9, bg_color=(250/255,5/255,25/255, 1), icon="login").open()
            except:
                CustomSnackbar(text="the account did not match our database /or/ The account is not registered", snackbar_x="10dp",
    snackbar_y="10dp",
    size_hint_x=.9, bg_color=(250/255,5/255,25/255, 1), icon="alert-circle").open()

            User.commit()

            User.close()
    def timing(self,d):
        try:
            if self.news_status == "Processing":
                self.ids.SC.remove_widget(self.ids.M)
                self.ids.spinner.checker = True
                self.ids.Username.disabled = True
                self.ids.Password.disabled = True
                self.ids.Register.disabled = True
                print("effective")

            elif self.news_status == "done":

                self.ids.screen_manager.current = "Main"


                plyer.notification.notify(title=f'Welcome to Gemys', message=f'details on email')


                self.ids.spinner.checker = False

            else:
                pass

        except:
            pass

    def Submit_Registration(self):

        if len(self.ids.Name_User.text) == 0 or len(self.ids.User_LastName.text) == 0 or len(
                self.ids.User_Password.text) == 0 or len(self.ids.User_email.text) == 0 or len(
                self.ids.User_day_birth.text) == 0 or len(self.ids.select_mo.text) == 0 or len(
                self.ids.User_year_birth.text) == 0:
            CustomSnackbar(text=f"Incomplete form", snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.9, bg_color=(250 / 255, 5 / 255, 25 / 255, 1),
                           icon='folder-information').open()
        else:

            User = mysql.connector.connect(
                host='localhost',
                user='root',
                passwd='mikyortiz1224@',
                database='second_database'

            )
            c = User.cursor()

            command = "INSERT INTO User_Registration(name, lastname, password, email, day, month, year) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            values = (self.ids.Name_User.text, self.ids.User_LastName.text,
                      self.ids.User_Password.text, self.ids.User_email.text,
                      self.ids.User_day_birth.text, self.ids.select_mo.text,
                      self.ids.User_year_birth.text,)
            print(self.ids.User_email.text)

            send_email.e_mail.User_email = self.ids.User_email.text
            send_email.e_mail.User_topic = f'Welcome To Gemys {self.ids.Name_User.text} {self.ids.User_LastName.text}'
            send_email.e_mail.User_message = f'Hey, {self.ids.Name_User.text} we are exited to have you as a member of our community\n ' \
                                             f'this is your id \n' \
                                             f'ID = {random.randint(50000, 100000)}'
            miky = send_email.e_mail()
            miky.User_email = f'{self.ids.User_email.text}'
            TT = threading.Thread(target=miky.sender)
            TT.start()

            c.execute(command, values)

            CustomSnackbar(text=f"Registration Completed", snackbar_x="10dp",
                           snackbar_y="10dp",
                           size_hint_x=.9, bg_color=(250 / 255, 5 / 255, 25 / 255, 1), icon='check').open()

            User.commit()

            User.close()
            self.ids.screen_manager.current = "login"

            self.ids.Name_User.text = ''
            self.ids.User_LastName.text = ''
            self.ids.User_Password.text = ''
            self.ids.User_email.text = ''
            self.ids.User_day_birth.text = '12'
            self.ids.select_mo.text = 'Select Month'
            self.ids.User_year_birth.text = '1998'




    def arrow_back(self):
        self.ids.screen_manager.current = "login"

MainLayout.capture.release()
cv2.destroyAllWindows()

class test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Red"


        return MainLayout()

    def on_start(self):

        # create database or connect

        # conn = sqlite3.connect("first_data.db")


        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='mikyortiz1224@',
            database='second_database'
        )

        # create a cursor

        c = mydb.cursor()



        # check if it was created

        """c.execute("SHOW DATABASES")
        for db in c:
            print(db)"""

        # create a database

        c.execute(""" CREATE DATABASE IF NOT EXISTS second_database""")

        # create table

        c.execute(""" CREATE TABLE if not exists User_Registration(
        name VARCHAR(50), lastname VARCHAR(50), password VARCHAR(15), email VARCHAR(50), day int(2), month VARCHAR(50), year int(4))
        """)

        # check to see if table was created

        """c.execute("SELECT password FROM User_Registration")
        print(c.description)"""

        # commint changes
        mydb.commit()

        mydb.close()

    def on_stop(self):

        MainLayout.cam_on_off = False
        print("stop")

        try:
            for i in range(len(MainLayout.countries)):
                shutil.rmtree(f"{MainLayout.countries[i]}")

        except:
            print('error')




if __name__ == '__main__':
    test().run()

