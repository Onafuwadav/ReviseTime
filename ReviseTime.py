from time import strftime

from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import *
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.config import Config
from datetime import date
import calendar
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from time import strftime
from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
import sqlite3
import random
import quickstart

con = sqlite3.connect('ReviseTime.db')
Builder.load_file("kivy.kv")

Config.set('graphics', 'fullscreen', 'fake')
Config.write()


class Screen_Manager(ScreenManager):
    pass


class TouchApp(MDApp):
    quickstart.main()
    dialog = None
    create = None

    def __init__(self, **kwargs):
        self.title = "ReviseTime"
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.primary_palette = "Green"  # "Purple", "Red"
        self.theme_cls.primary_hue = "300"  # "500"
        return Screen_Manager()

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
                      "VALUES (?, ?, ?)")
            data = (self.dialog.content_cls.ids.forename.text, self.dialog.content_cls.ids.email.text,
                    self.dialog.content_cls.ids.password.text)
            cur.execute(insert, data)
            con.commit()
            insert = ("INSERT INTO Subjects(H1, H2, H3, S1, S2, S3)"
                      "VALUES (?, ?, ?, ?, ?, ?)")
            data = (self.create.content_cls.ids.HL1.text, self.create.content_cls.ids.HL2.text,
                    self.create.content_cls.ids.HL3.text, self.create.content_cls.ids.SL1.text,
                    self.create.content_cls.ids.SL2.text, self.create.content_cls.ids.SL3.text)
            cur.execute(insert, data)
            con.commit()
            con.close()
            self.create.dismiss()

    def previous_page(self, obj):
        self.create.dismiss()
        self.signup()

    def signin(self, obj):
        id = self.root.get_screen('start')
        if id.ids.email.text == "1" and id.ids.passwd.text == "2":
            id.ids.email.text = ''
            id.ids.passwd.text = ''
            return True
        else:
            return False


class WeeklyTimetable(Screen):
    def datatable(self):
        self.data_tables = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.7),
            column_data=[
                ("Pic", dp(20)),
                ("Monday", dp(35)),
                ("Tuesday", dp(35)),
                ("Wednesday", dp(35)),
                ("Thursday", dp(35)),
                ("Friday", dp(35)),
                ("Saturday", dp(35)),
                ("Sunday", dp(35))
            ],
            row_data=[
                (
                    "1 pm",
                    "School",
                    "School",
                    "School",
                    "School",
                    "School",
                    "EE",
                    "EE",
                ),
                (
                    "2 pm",
                    "School",
                    "School",
                    "School",
                    "School",
                    "School",
                    "Revision",
                    "Revision",
                ),
                (
                    "3 pm",
                    "School",
                    "School",
                    "School",
                    "School",
                    "School",
                    "hw",
                    "hw",
                ),
                (
                    "4 pm",
                    "Break",
                    "Break",
                    "Break",
                    "Break",
                    "Break",
                    "Break",
                    "Break",
                ),
                (
                    "5 pm",
                    "EE",
                    "EE",
                    "EE",
                    "EE",
                    "EE",
                    "EE",
                    "EE",
                ),
                (
                    "6 pm",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                ),
                (
                    "7 pm",
                    "IA",
                    "IA",
                    "IA",
                    "IA",
                    "IA",
                    "IA",
                    "IA",
                ),
                (
                    "8 pm",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                ),
                (
                    "9 pm",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                    "Revision",
                ),
                (
                    "10 pm",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                    "hw",
                ),
            ],
        )
        layout = AnchorLayout()
        layout.add_widget(self.data_tables)
        self.add_widget(layout)


class MainMenu(Screen):
    def on_row_press_weekday(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        copy2 = quickstart.dates.copy()
        if current_row.index == 7:
            breaktime = MDDialog(title="BreakTime", text="Take a break! :)")
            breaktime.open()
        if current_row.index == 9:
            EE = MDDialog(title="EE", text="Time to do your EE")
            EE.open()
        if current_row.index == 11:
            hw1d = MDDialog(title="Hw Description", text=str(copy2[0][2]))
            hw1d.open()
        if current_row.index == 13:
            IA = MDDialog(title="IA", text="Make list of subjects and choose i from randon.choice")
            IA.open()
        if current_row.index == 17:
            Revision = MDDialog(title="Revision", text="Make list of subjects and choose i from randon.choice")
            Revision.open()
        if current_row.index == 19:
            hw3d = MDDialog(title="Hw Description", text=str(copy2[1][2]))
            hw3d.open()
        if current_row.index == 1 or current_row.index == 3 or current_row.index == 5:
            quotes = ["Education is the most powerful weapon which you can use to change the world",
                      "Education is the key to unlocking the world, a passport to freedom",
                      "Education is not preparation for life; education is life itself",
                      "Education is the passport to the future, for tomorrow belongs to those who prepare for it today",
                      "Upon the subject of education … I can only say that I view it as the most important subject "
                      "which we as a people may be engaged in."]
            quote = random.choice(quotes)
            schoold = MDDialog(title="School Time", text=quote)
            schoold.open()
        else:
            print('hi')

    def on_row_press_weekend(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        copy2 = quickstart.dates.copy()
        if current_row.index == 7:
            breaktime = MDDialog(title="BreakTime", text="Take a break! :)")
            breaktime.open()
        if current_row.index == 9 or current_row.index == 1:
            EE = MDDialog(title="EE", text="Time to do your EE")
            EE.open()
        if current_row.index == 5:
            hw1d = MDDialog(title="Hw Description", text=str(copy2[0][2]))
            hw1d.open()
        if current_row.index == 11:
            hw2d = MDDialog(title="Hw Description", text=str(copy2[1][2]))
            hw2d.open()
        if current_row.index == 13:
            IA = MDDialog(title="IA", text="Make list of subjects and choose i from randon.choice")
            IA.open()
        if current_row.index == 17 or current_row.index == 15 or current_row.index == 3:
            Revision = MDDialog(title="Revision", text="Make list of subjects and choose i from randon.choice")
            Revision.open()
        if current_row.index == 19:
            hw3d = MDDialog(title="Hw Description", text=str(copy2[2][2]))
            hw3d.open()
        else:
            print("hi")

    def datatable(self):
        copy = quickstart.dates.copy()
        self.weekday = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.3, 0.7),
            column_data=[
                ('pic', dp(20)),
                (calendar.day_name[date.today().weekday()], dp(55)),
            ],
            row_data=[
                (
                    "1 pm",
                    "School",
                ),
                (
                    "2 pm",
                    "School",
                ),
                (
                    "3 pm",
                    "School",
                ),
                (
                    "4 pm",
                    "Break",
                ),
                (
                    "5 pm",
                    "EE",
                ),
                (
                    "6 pm",
                    str(copy[0][1]),
                ),
                (
                    "7 pm",
                    "IA",
                ),
                (
                    "8 pm",
                    "Revision",
                ),
                (
                    "9 pm",
                    "Revision",
                ),
                (
                    "10 pm",
                    str(copy[2][1]),
                ),
            ],
        )
        copy = quickstart.dates.copy()
        self.weekend = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.3, 0.7),
            column_data=[
                ('pic', dp(20)),
                (calendar.day_name[date.today().weekday()], dp(55)),
            ],
            row_data=[
                (
                    "1 pm",
                    "EE",
                ),
                (
                    "2 pm",
                    "Revision",
                ),
                (
                    "3 pm",
                    str(copy[0][1]),
                ),
                (
                    "4 pm",
                    "Break",
                ),
                (
                    "5 pm",
                    "EE",
                ),
                (
                    "6 pm",
                    str(copy[1][1]),
                ),
                (
                    "7 pm",
                    "IA",
                ),
                (
                    "8 pm",
                    "Revision",
                ),
                (
                    "9 pm",
                    "Revision",
                ),
                (
                    "10 pm",
                    str(copy[2][1]),
                ),
            ],
        )
        layout = AnchorLayout()
        if date.today().weekday() < 5:
            layout.add_widget(self.weekday)
            self.weekday.bind(on_row_press=self.on_row_press_weekday)
        else:
            layout.add_widget(self.weekend)
            self.weekend.bind(on_row_press=self.on_row_press_weekend)
        self.add_widget(layout)


class SignUpScreen(BoxLayout):
    some_variable = TouchApp()
    pass


class SignUpScreen2(BoxLayout):
    some_variable = TouchApp()
    pass


class Settings_Screen(Screen):
    pass


class Timers(Screen):
    sw_started = False
    sw_seconds = 0

    def update_time(self, nap):
        if self.sw_started:
            self.sw_seconds += nap
        minutes, seconds = divmod(self.sw_seconds, 60)
        self.root.ids.stopwatch.text = (
            '%02d:%02d.[size=40]%02d[/size]'%
            (int(minutes), int(seconds),
             int(seconds* 100 % 100))
        )
        self.root.ids.time.text = strftime('[b]%H[/b]:%M:%S')

    def on_start(self):
        Clock.schedule_interval(self.update_time, 0)

    def start_stop(self):
        self.root.ids.start_stop.text =(
            'Start' if self.sw_started else 'Stop'
        )
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False
        self.sw_seconds = 0


class TestDates(Screen):
    pass


class StartScreen(Screen):
    pass


if __name__ == "__main__":
    TouchApp().run()
