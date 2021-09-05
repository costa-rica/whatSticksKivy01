from kivymd.app import MDApp
# from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests
import json
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
import datetime;from datetime import timedelta



class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(LoginWindow, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()
    
    def loginBtn(self):
        response = requests.request('GET','http://api.what-sticks-health.com/get_users',
            auth=(self.email.text,self.password.text))
        
        print('response.status_code:::', response.status_code)
        if response.status_code ==200:
            for i in json.loads(response.content.decode('utf-8')):
                if i['email']==self.email.text:
            
                    # WindowList.current = self.email.text#get user for main window
                    # WindowList.user_id1=i['id']
                    # WindowList.user_name1=i['username']
                    # WindowList.user_timezone1=i['user_timezone']
                    # WindowList.email1=i['email']
                    # WindowList.password1=self.password.text
                    
                    WindowAdd.user_name_str=i['username']
                    WindowAdd.user_id_str=i['id']
                    WindowAdd.email_str=i['email']
                    
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
    user_id = ObjectProperty(None)
    user_id_str=''
    email = ObjectProperty(None)
    email_str=''
    
    
    current=''
    

    
    def __init__(self, **kwargs):
        super(WindowAdd, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()


    def on_enter(self,*args):
        self.user_name.text='User Name: '+self.user_name_str
        self.user_id.text='ID: '+str(self.user_id_str)
        self.email.text='Email: '+self.email_str


class WindowList(Screen):
    user_id = ObjectProperty(None)
    # user_name = ObjectProperty(None)
    # user_timezone= ObjectProperty(None)
    # email = ObjectProperty(None)
    current = ""
    user_id1=''
    user_name1=''
    user_timezone1=''
    email1=''
    password1=''
    # print('email1:::',self.email1)
    

    def __init__(self, **kwargs):
        super(WindowList, self).__init__(**kwargs)
        self.app=WhatSticksHealth.get_running_app()
        self.data_table=None

    def logOut(self):
        sm.current = 'login'

    def on_enter(self,*args):
        self.user_id.text='User ID: '+self.current
        print('email1:::',self.email1)
        
        response = requests.request('GET','http://api.life-buddy.org/get_health_descriptions',
            auth=(self.email1,self.password1))
        print(response.status_code)
        #put data into list of tuples
        response_data=json.loads(response.content.decode('utf-8'))
        row_data_list=[("[size=12]"+self.convert_datetime(i['datetime_of_activity']),"[size=12]"+i['var_activity']) for i in response_data]
        
        self.data_table_card=MDDataTable(size_hint=(.6,.8),
            use_pagination=True,
            column_data=[("[size=15]Date/Time", dp(50)),("[size=15]Exercise", dp(30))],
            row_data=row_data_list)
        self.add_widget(self.data_table_card)

    def convert_datetime(self,date_time_str):
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
        self.theme_cls.theme_style ="Dark"
        self.theme_cls.primary_palette = "DeepOrange"

        self.sm = WindowManager()
        
        self.sm.add_widget(LoginWindow(name="login"))
        self.sm.add_widget(WindowAdd(name="activity_add"))
        self.sm.add_widget(WindowList(name="activity_list"))
            
        self.sm.current = "login"
        
        
        
        
        return self.sm


if __name__ == "__main__":
    WhatSticksHealth().run()
    
            