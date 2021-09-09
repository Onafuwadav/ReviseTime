from kivy.app import *
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivymd.uix.behaviors.backgroundcolor_behavior import *
from kivy.uix.boxlayout import *
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivymd import app
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy import utils
import sqlite3

con = sqlite3.connect('ReviseTime.db')

Builder.load_file("kivy.kv")


class TouchApp(MDApp):
    dialog = None
    create = None

    def __init__(self, **kwargs):
        self.title = "ReviseTime"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "300"  # "500"
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        return sm

    def signup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Personal Information:",
                size_hint=[0.5, None],
                auto_dismiss=False,
                type="custom",
                content_cls=SignUpScreen(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color, on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Next page", text_color=self.theme_cls.primary_color, on_release=self.next_page
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def next_page(self, obj):
        if self.dialog.content_cls.ids.forename.text != "" and self.dialog.content_cls.ids.email.text != '' and \
                self.dialog.content_cls.ids.password.text != '' and self.dialog.content_cls.ids.password2.text != '':
            if len(self.dialog.content_cls.ids.password.text) >= 8:
                if self.dialog.content_cls.ids.password.text == self.dialog.content_cls.ids.password2.text:
                    self.dialog.content_cls.ids.error.text = ""
                    self.dialog.dismiss()
                    self.signup2()
                else:
                    self.dialog.content_cls.ids.error.text = "Password and re-entered password must be the same!"
            else:
                self.dialog.content_cls.ids.error.text = "Password must be 8 characters!"
        else:
            self.dialog.content_cls.ids.error.text = "Please enter all required information!"

    def signup2(self):
        if not self.create:
            self.create = MDDialog(
                title="Subjects:",
                size_hint=[0.5, None],
                auto_dismiss=False,
                type="custom",
                content_cls=SignUpScreen2(),
                buttons=[
                    MDFlatButton(
                        text="Previous Page", text_color=self.theme_cls.primary_color, on_release=self.previous_page
                    ),
                    MDFlatButton(
                        text="Create account", text_color=self.theme_cls.primary_color, on_release=self.create_account
                    ),
                ],
            )
        self.create.open()

    def create_account(self, obj):
        check = True
        subjects = [self.create.content_cls.ids.HL1.text, self.create.content_cls.ids.HL2.text,
                    self.create.content_cls.ids.HL3.text, self.create.content_cls.ids.SL1.text,
                    self.create.content_cls.ids.SL2.text, self.create.content_cls.ids.SL3.text]
        for x in range(6):
            if x == "":
                check = False
        for x in range(5):
            for y in range(x + 1, 6):
                if subjects[x] == subjects[y]:
                    check = False
                    self.create.content_cls.ids.error.text = "No two subjects can be the same!"
                    break
                else:
                    continue
            if not check:
                break
        if check:
            self.create.content_cls.ids.error.text = ""
            cur = con.cursor()
            insert = ("INSERT INTO Settings(Name, Email, Password)"
                      "VALUES (%s, %s, %s)")
            data = (self.dialog.content_cls.ids.forename.text, self.dialog.content_cls.ids.email.text,
                    self.dialog.content_cls.ids.password.text)
            cur.execute(insert, data)
            con.commit()
            cur.execute("SELECT * FROM Settings")
            print(cur.fetchall())
            con.close()
            self.create.dismiss()

    def previous_page(self, obj):
        self.create.dismiss()
        self.signup()


class SignUpScreen(BoxLayout):
    some_variable = TouchApp()
    pass


class SignUpScreen2(BoxLayout):
    some_variable = TouchApp()
    pass


class StartScreen(Screen):
    Window.size = (500, 600)
    btn = ObjectProperty(None)

    def signin(self):
        if self.ids.email.text == "Davefuwa127" and self.ids.passwd.text == "Davefuwa":
            print("welcome")


if __name__ == "__main__":
    TouchApp().run()
