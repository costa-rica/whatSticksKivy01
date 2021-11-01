import sys
sys.path.append("_applibs")
sys.path.append(".")
from kivymd.app import MDApp
# from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, ColorProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests
import json
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
import datetime;from datetime import timedelta

from kivy.core.window import Window
Window.size = (300, 500)

from utils import add_activity_util, current_time_util

#from kivymd.uix.picker import MDDatePicker, MDTimePicker

import time
import pytz
# import zoneinfo
from pytz import timezone
import datetime;from datetime import timedelta

from kivy.factory import Factory
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
# from kivy.properties import (StringProperty, ObjectProperty, OptionProperty,
                             # NumericProperty, ColorProperty)


class WindowLogin(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(WindowLogin, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()

    def loginBtn(self):
        response = requests.request('GET','http://api.what-sticks-health.com/get_users',
            auth=(self.email.text,self.password.text))

        print('Login: response.status_code:::', response.status_code)
        if response.status_code ==200:
            for i in json.loads(response.content.decode('utf-8')):
                if i['email']==self.email.text:

                    WindowAdd.user_name_str=i['username']
                    WindowAdd.user_timezone=i['user_timezone']
                    WindowAdd.user_id_str=i['id']
                    WindowAdd.user_email=self.email.text
                    WindowAdd.user_password=self.password.text
                    self.reset()

                    #sm.current = 'main'
                    self.app.sm.current = 'activity_add'
        else:
            invalidLogin()

    def reset(self):
        self.email.text=''
        self.password.text=''

class WindowAdd(Screen):
    user_name = ObjectProperty(None)
    user_name_str=''
    user_id_str=''
    user_email=''
    user_password=''
    user_timezone=''
    title = ObjectProperty(None)
    note = ObjectProperty(None)
    time_thing=ObjectProperty(None)
    current=''

    def __init__(self, **kwargs):
        super(WindowAdd, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()
        self.date_time_obj=datetime.datetime.now()

    def on_enter(self,*args):
        self.user_name.text=self.user_name_str
        # self.user_id.text='ID: '+str(self.user_id_str)
        # self.email.text='Email: '+self.email_str
        self.date_time_now=current_time_util(self.user_timezone)
        self.ids.date_thing.text=self.date_time_now[0]
        self.ids.time_thing.text=self.date_time_now[1]

    def logOut(self):
        self.app.sm.current = 'login'


    def toWindowList(self):
        WindowList.user_email=self.user_email
        WindowList.user_password=self.user_password
        WindowList.user_id_str=self.user_id_str
        WindowList.user_name_str=self.user_name_str
        self.app.sm.current = 'activity_list'

    def logActivity(self):
        title=self.title.text
        note=self.note.text

        #combine date_thing adn time_thing into datetime object
        try:
            print('datetime_thing string:::',self.ids.date_thing.text +" "+ self.ids.time_thing.text)
            datetime_thing=datetime.datetime.strptime(self.ids.date_thing.text +" "+ self.ids.time_thing.text,'%m/%d/%Y %I:%M %p')
            add_activity_util(title, note,self.user_id_str,self.user_timezone,datetime_thing, self.user_email,self.user_password)
            content=GridLayout(cols=1)
            popup_success = Popup(title='Successfully submitted',size_hint=(None, None),
                size=(256, 60),content=content, disabled=True,title_color = "green")
            popup_success.open()

        except ValueError:
            content=GridLayout(cols=1)
            popup_error = Popup(title='Date/Time Wrong Format',size_hint=(None, None), size=(256, 60),
                content=content, disabled=True,title_color = "orange")
            popup_error.open()



class WindowList(Screen):
    user_id = ObjectProperty(None)
    # user_name = ObjectProperty(None)
    # user_timezone= ObjectProperty(None)
    # email = ObjectProperty(None)
    current = ""
    user_id_str=''
    user_name_str=''
    user_timezone1=''
    user_email=''
    user_password=''
    # print('email1:::',self.email1)


    def __init__(self, **kwargs):
        super(WindowList, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()
        self.data_table=None

    def logOut(self):
        self.app.sm.current = 'login'

    def on_enter(self,*args):
        print('args:::',*args)
        self.user_id.text='User: '+self.user_name_str
        print('user_email:::',self.user_email)

        url='https://api.what-sticks-health.com/get_health_descriptions/' + str(self.user_id_str)
        print('url::',url)
        print('self.user_email:::',self.user_email)
        print('self.user_password:::',self.user_password)
        response = requests.request('GET',url,auth=(self.user_email,self.user_password))
        print(response.status_code)
        #put data into list of tuples
        response_decoded=response.content.decode('utf-8')
        print('response:::', type(response_decoded),response_decoded)

        response_data=json.loads(response.content.decode('utf-8'))
        print('response_data:::',type(response_data),response_data)
        print('response_data[datetime]:::',response_data['datetime_of_activity'])
        row_data_list=[(self.convert_datetime(i['datetime_of_activity']),i['var_activity']) for i in response_data]
        print('row_data_list:::',row_data_list)
        # row_data_list=[("[size=12]"+self.convert_datetime(i['datetime_of_activity']),"[size=12]"+i['var_activity']) for i in response_data]

        self.data_table_card=MDDataTable(size_hint=(.6,.8),
            use_pagination=True,
            column_data=[("[size=15]Date/Time", dp(50)),("[size=15]Exercise", dp(30))],
            row_data=row_data_list)
        self.add_widget(self.data_table_card)

    def convert_datetime(self,date_time_str):
        print('are we even getting here????')
        try:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%f')
        except ValueError:
            date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
        return date_time_obj.strftime("%m/%d/%Y, %H:%M:%S")



class WindowManager(ScreenManager):
    pass


def invalidLogin():
    pop = Popup(title='Invalid Login',
                  content=Label(text='Invalid username or password.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()


def invalidForm():
    pop = Popup(title='Invalid Form',
                  content=Label(text='Please fill in all inputs with valid information.'),
                  size_hint=(None, None), size=(400, 400))

    pop.open()


kv = Builder.load_file("kivyDesign.kv")

def info():
    print(dir(self.app.root))


def add_label(self):
    print('add_label--did this activate?')
    self.label_card=MDLabel(text="Test",halign="center")
    self.add_widget(self.label_card)




class WhatSticksHealth(MDApp):#app

    def build(self):
        self.icon = "tgelogo20210830_v2.png"
        self.theme_cls.theme_style ="Light"
        self.theme_cls.primary_palette = "DeepOrange"



        self.sm = WindowManager()

        self.sm.add_widget(WindowLogin(name="login"))
        self.sm.add_widget(WindowAdd(name="activity_add"))
        self.sm.add_widget(WindowList(name="activity_list"))

        self.sm.current = "login"




        return self.sm


if __name__ == "__main__":
    WhatSticksHealth().run()
