################################################
# FIRST REAL GUI U reSING KIVY                    #
# FIRST FULLY FUNCTIONAL RISK MANAGER APP      #
# OFFICIAL VERSION 3.0                         #
# RISKMAN STUDIO                               #
################################################

# KIVY IMPORTS
from logging import root
import kivy
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
kivy.require('2.0.0')
from kivy.config import Config
from kivy.uix.screenmanager import Screen
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '600')
Config.write()

from sys import maxsize
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.factory import Factory
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup

from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.tab import MDTabs
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager
from kivymd.uix.datatables import MDDataTable, TableHeader, TableData, TablePagination
from kivymd.uix.dialog import BaseDialog
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.label import MDLabel

# DATABASE IMPORTS
from IPython.display import display
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, MetaData, Table, select, delete
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.expression import null
from sqlalchemy import column
from sqlalchemy import create_engine
from sqlalchemy import select
from sqlalchemy import table
from sqlalchemy import text
from sqlalchemy import Integer

from functools import partial #Used in Clock.schedule_once

# ACCOUNT API IMPORTS
from rm_questrade_api import *
# CUSTOM FUCITION IMPORTS
from rm_tables import *
import rm_tables
import time

# ------------ SETUP DATABASE -------------
aws = "postgresql+psycopg2://riskmit:Cracker70@usefulanalytics-instance.cjepocpyhpgj.us-east-2.rds.amazonaws.com/riskmit"
engine = create_engine(aws, echo=False)
#Session = sessionmaker(bind=engine) # create a configured "Session" class   
#Session = sessionmaker(engine)
#session = Session() # create a Session
metadata = MetaData()
Base = declarative_base()

# Database operations
class DataBase():
    def get_all_users():
        s = "SELECT active, user_name, password, first_name, last_name, email FROM users"
        with engine.begin() as connection: #Open database and auto commit
            result = connection.execute(s)
            print("results : ",result)
        data = []
        for x in result:
            data.append(x)
        return data
    def get_user(username):
        s = select(Users).where(Users.user_name == username)
        with engine.begin() as connection: #Open database and auto commit
            result = connection.execute(s).fetchone()
        return result
    def update_user(username):
        pass
# MAIN SCREENS
class ScreenLogin(Screen):
    def login(self,username,password):
        print('Login!')
        username = username.text
        password = password.text
        #get password from db
        print ('Using:    Username : ', username,"   Password :",password)
        s = select(Users).where(Users.user_name == username)
        with engine.begin() as connection: #Open database and auto commit
            result = connection.execute(s)
            print("results : ",result)
        first_name = 'Does Note Exist'
        last_name = 'Does Note Exist'
        password_actual = 'Does Note Exist'
        username_actual = 'Does Note Exist'
        for object in result:
            try:
                print('object :',object)
                username_actual = object.user_name
                first_name = object.first_name
                last_name = object.last_name
                password_actual = object.password
            except:
                print('This is run because username is not found')
        print('actual values :', first_name, last_name, password_actual, username_actual)
        
        if username_actual == username and password_actual == password:
            print("you may pass")
            #app.ids.welcome_label.text = 'AUTHORIZED!'
            #app.screen_manager.current = 'overview'
        elif username_actual == username:
            print ('INCORECT PASSWORD')
        else:
            print("INCORRECT USERNAME")
            self.manager.current = "screen_main"
            print("it should of worked bynow")
            #self.ids.welcome_label.text = "INCORRECT USERNAME"
            #self.ids.password.text = ""
    def register(self):
        print("register!")
        AppScreenManager.current = ScreenRegistration()
class ScreenRegistration(Screen):
    def __init__(self, **kw):
        super(ScreenRegistration,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        pass
        #Window.size = (500,500)  
class ScreenSuperuser(Screen):
    def __init__(self, **kw):
        super(ScreenSuperuser,self).__init__(**kw)
    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel oject>;
        :param tab_text: text or name icon of tab;
        '''
        #get the tab icon
        count_icon = instance_tab.icon
        tab_name = instance_tab.title
        print("instance_tab :",instance_tab)
        print(f"Welcome to {tab_name}")
        #if tab_name == "USERS":
        #    TabUsers.load_data(self)
    def back_button(self):
        self.parent.current='overview'
    def create_tables(self):
        print("I'm going to create the tables now")
        rm_tables.Base.metadata.create_all(engine)
        print('Tables Created')
    #def on_enter(self):
        #Clock.schedule_once(self.load_data)
    def load_data(self):
        print("Thiis is loading on superuser entery")
        data_users = DataBase.get_all_users()
        print("data_users : ",data_users)
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    content_text = StringProperty("")   
class TabUsers(Tab):
    def __init__(self, **kwargs):
        super(TabUsers, self).__init__(**kwargs)
        Clock.schedule_once(self.display_users)
    def display_users(self,*args):
        global check_pressed
        check_pressed = False
        #screen_superuser = ObjectProperty()
        #tab_users = ObjectProperty()
        print('running load data')
        data = DataBase.get_all_users()
        print("data is goig to be :",data)
        self.table_users = MDDataTable(
            size_hint = (.9,.8),
            use_pagination=False,
            rows_num = 10,
            check = True,
            elevation = 20,
            pos_hint = {'center_x': .5, 'top': 1},
            column_data = [("Active",dp(30)),("UserName", dp(30)),("Password", dp(30)),("First Name",dp(30)),("Last Name",dp(30)),("Email",dp(40))],
            row_data = data,
            )
        self.add_widget(self.table_users)
        print("table is added")
        self.table_users.bind(on_row_press=self.on_row_press)
        self.table_users.bind(on_check_press=self.on_check_press)
        
    def popup_user(self,user_record):
        global check_pressed
        show = PopupUserContent()
        popup = Popup(title='EDIT USER',
            content=show,
            size_hint=(.6, .8)
            #size=(400, 400)
            )
        if check_pressed == True:
            popup.dismiss()
            check_pressed = False
        else:
            popup.open()

    def on_row_press(self, table, row): #user row clicked - open pop up to edit
        '''Called when a table row is clicked.'''
        print("row was clicked : ", table,row)
        start_index, end_index = row.table.recycle_data[row.index]["range"]
        username = row.table.recycle_data[start_index + 1]["text"]
        print("username sElected : ", username)
        user_record = DataBase.get_user(username) # get full record from database to populate pop up
        print("user record : ",user_record)
        self.popup_user(user_record)

    def on_check_press(self, instance_table, current_row):
        global check_pressed
        '''Called when the check box in the table row is checked.'''
        time.sleep(.025)
        print("on check was pressed : ",instance_table, current_row)
        print("on_check Press : current row", current_row)
        check_pressed = True
        #self.popup_user("dismiss")
class PopupUserContent(MDFloatLayout):
    pass
class TabBrokers(Tab):
    pass
class TabAccounts(Tab):
    pass
class ScreenMain(Screen):
    def __init__(self, **kw):
        super(ScreenMain,self).__init__(**kw)

    def toggle_nav_drawer(self):
        print("navigation toggle")
class ContentNavigationDrawer(MDBoxLayout):
    #screen_manager = ObjectProperty()
    #nav_drawer = ObjectProperty()
    pass

# MAIN SCREENS
class ScreenOverview(Screen):
    def __init__(self, **kw):
        super(ScreenOverview,self).__init__(**kw)
    
    def on_pre_enter(self, *args):
        #Window.maximize
        pass
        #Window.size = (1000,600)

    def log_out(self):
        s1 = self.manager.get_screen('screen_login')
        s1.ids.welcome_label.text = "LOGIN"
        self.parent.current = 'screen_login'
class PostionsScreen(Screen):
    pass
class OrdersScreen(Screen):
    pass
class BidsScreen(Screen):
    pass
class TradeScreen(Screen):
    pass
class JournalScreen(Screen):
    pass
class SettingsScreen(Screen):
    pass

# SCREEN MANAGERS
class ScreenManagerApp(ScreenManager):
    screen_login = ObjectProperty()
    screen_registration = ObjectProperty()
    screen_main = ObjectProperty()
    screen_superuser = ObjectProperty()

    def change_screen(self, screen):
        self.current = screen

    def open_superuser(self):
        print("Opening settings")
        self.parent.current = 'super_user'

    #def __init__(self, **kwargs):
     #   super(App.ScreenManager, self).__init__(**kwargs) 
class ScreenManagerMain(ScreenManager):
    overview = ObjectProperty()
    positions = ObjectProperty()
    orders = ObjectProperty()
    def __init__(self, **kwargs):
        super(ScreenManagerMain, self).__init__(**kwargs)

    #def open_superuser(self):
        #print("Open Superuser!")

# ========== MAIN CLASS =========================
class RiskManager(MDApp):
    #theme_cls = ThemeManager()
    
    # SET TITLE AND ICON
    def __init__(self, **kwargs):
        self.title = "RiskManager"
        self.icon = "assets/fgwhite.png"
        
        super().__init__(**kwargs)
        
    # BUILD THE UI
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette ="Blue"
        self.theme_cls.accent_palette = "Red"
                       
        return Builder.load_file('riskman.kv')

# ======== RUN APP =======================    
if __name__ == '__main__':
    RiskManager().run()
