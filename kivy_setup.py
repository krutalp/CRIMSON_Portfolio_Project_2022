from kivy.app import App
# installing kivy requires the following: pip install kivy[base] kivy_examples --pre --extra-index-url https://kivy.org/downloads/simple/
from kivy.uix.widget import Widget 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
import json
import requests
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
import multiprocessing
from multiprocessing import dummy
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty
from kivy.uix.label import Label
from kivy.uix.button import Button

# CONNECTOR method with app component 2
from main_app import attentionApp

import random
import time
random.seed(time.process_time())


sm = ScreenManager()

class WindowManager(ScreenManager):
    pass

class MainWindow(Screen):
    pass

class Login(Screen):
    pass

class Signup(Screen):
    pass

class Information(Screen):
    pass

class Signupsuccess(Screen):
    pass

class StartScreen11(Screen):
   pass

class MainWidget(Widget):
    pass

class Data(Screen):
    pass

# all instances referenced through this command: run App main here
class PortfolioApp(MDApp, App):
    def build(self):
        #Window.clearcolor = (0/255,191/255,255/255,1)
        #self.theme_cls.theme_Style = 'dark'
        #self.theme_cls.primary_palette = 'BlueGray'
        self.kv = Builder.load_file('PortfolioApp.kv')
        self.url = "https://friedbrainsapp-default-rtdb.firebaseio.com/.json"
        return self.kv
    
    def signup(self):
        # extract type(Str) inputs from user kivyMD text input
        name = self.kv.get_screen('Signup').ids.user.text
        username = self.kv.get_screen('Signup').ids.username.text
        password = self.kv.get_screen('Signup').ids.pw.text

        if name.split() == [] or username.split() == [] or password.split() == []:
            cancel_btn_user_bx = MDFlatButton(text = 'Try again', on_release = self.close_user_bx)
            
            self.dialog = MDDialog(title = 'Invalid', text = 'Please enter all information correctly', size_hint = (0.7,0.2), buttons = [cancel_btn_user_bx])
            self.dialog.open()
            self.kv.get_screen('Signup').manager.current = 'Signup'

        elif len(name.split()) > 1:
            cancel_btn_user_bx = MDFlatButton(text = 'Retry', on_release = self.close_user_bx)
            self.dialog = MDDialog(title = 'Invalid', text = 'Please enter all information correctly', size_hint = (0.7,0.2), buttons = [cancel_btn_user_bx])
            self.dialog.open()
            self.kv.get_screen('Signup').manager.current = 'Signup'
        else:
            print(name, password)
            signup_data = str({f'\"{name}\":{{"Password":\"{password}\","Username":\"{username}\"}}'})
            signup_data = signup_data.replace(".","-")
            signup_data = signup_data.replace("\'","")
            to_database = json.loads(signup_data)
            requests.patch(url = self.url,json = to_database)
            self.kv.get_screen('signupsuccess').manager.current = 'signupsuccess'
            

    auth = "6epJPA2oIWiu8IA9n6ZIwUjQUw9bFIkPcV9phAmf"

    def login(self):
        login_user = self.kv.get_screen('Login').ids.user.text
        login_password = self.kv.get_screen('Login').ids.pw.text

        self.login_check = False
        database_supported_user = login_user.replace('.','-')
        database_supported_pw = login_password.replace('.','-')

        request  = requests.get(self.url+'?auth='+self.auth)

        data = request.json()

        uns = set()

        for key,value in data.items():
            uns.add(key)
        if database_supported_user in uns and database_supported_pw == data[database_supported_user]['Password']:
            self.user = data[database_supported_user]['Username']
            self.login_check = True
            self.kv.get_screen('StartScreen11').manager.current = 'StartScreen11'

        else:
            print("invalid login attempt.Try again")
            cancel_btn_user_bx = MDFlatButton(text = 'Retry', on_release = self.close_user_bx)
            self.dialog = MDDialog(title = 'Invalid', text = 'Try again', size_hint = (0.7,0.2), buttons = [cancel_btn_user_bx])
            self.dialog.open()


    def storeData(self):
        acc_Rate = self.kv.get_screen('Data').ids.acc_rate.text
        Time = self.kv.get_screen('Data').ids.times.text
        click_count = self.kv.get_screen('Data').ids.ckct.text 
        name = self.kv.get_screen('Signup').ids.user.text

        push_data = str({f'\"{name}\":{{"acc_Rate":\"{acc_Rate}\","Time":\"{Time}\"}}'})
        push_data = push_data.replace(".","-")
        push_data = push_data.replace("\'","")

        to_database = json.loads(push_data)
        requests.patch(url = self.url,json = to_database)


    
    def close_user_bx(self,obj):
        self.dialog.dismiss()

    def username_changer(self):
        if self.login_check:
            self.kv.get_screen('StartScreen11').manager.current = 'StartScreen11'

    def launchGame(self):
        app = attentionApp()
        app.run()

    def close_app(self):
        App.get_running_app().stop()
        Window.close()


if __name__ == '__main__':
    PortfolioApp().run() 
