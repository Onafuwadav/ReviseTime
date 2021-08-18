from kivy.app import *
from kivy.uix.boxlayout import *
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivymd.uix.card import MDCard
from kivy.core.window import Window


class TouchApp(MDApp):
    def __init__(self, **kwargs):
        self.title = "ReviseTime"
        super().__init__(**kwargs)

    def build(self):
        return StartScreen()


class Sign_Up_Screen(BoxLayout):
    btn = ObjectProperty(None)

    def login(self, email, password):
        if email == "Davefuwa127" and password == "Davefuwa":
            print("welcome")


class StartScreen(BoxLayout):
    Window.size = (500, 600)
    btn = ObjectProperty(None)

    def SignUpScreens(self):
        SignUpScreen.open()


Builder.load_string("""
#:include kivy.kv

#:import utils kivy.utils

""")

SignUpScreen = Popup(title='Sign Up',
                     content=Sign_Up_Screen(), size_hint=(None, None), size=(400, 600))


if __name__ == "__main__":
    TouchApp().run()
