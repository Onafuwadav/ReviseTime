import os

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import *
from kivy.uix.checkbox import CheckBox
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.config import Config
from datetime import date, datetime
from kivy.lang import Builder
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
import calendar
import sqlite3
import random
from kivymd.uix.snackbar import Snackbar
import quickstart
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.picker import MDDatePicker
import time

con = sqlite3.connect('ReviseTime.db')
cur = con.cursor()
Builder.load_file("kivy.kv")
Config.set('graphics', 'resizeable', 1)
Config.set('graphics', 'position', "auto")
Config.write()
sm = ScreenManager()


class TestDates(Screen):
    dialog = None

    def delete(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete deadline?",
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Cancel", on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Confirm", on_release=lambda x: self.cancel()
                    ),
                ],
            )
        self.dialog.open()

    def cancel(self):
        for child in reversed(sm.get_screen('testDates').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    if c.active:
                        title = child.title
                        desc = child.description
        # remove from text file
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                desc_days = time.strptime(str(desc).strip('\n'), "%d/%m/%Y")
                today = date.today()
                today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                days = int((time.mktime(desc_days) - time.mktime(today1)) // 86400)
                if line.strip('\n') == str(days)+','+str(title)+','+str(desc).strip('\n'):
                    lines.remove(line)
        with open('Dates.txt', 'w') as f:
            x = 0
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            for line in lines:
                f.write(line+'\n')
        self.close_dialog(self.dialog)
        for elements in sm.get_screen('testDates').ids.todo_list.children:
            if elements.ids.title.text == title and elements.ids.description.text == desc:
                elements.parent.remove_widget(elements)
                for child in reversed(sm.get_screen('testDates').ids.todo_list.children):
                    for c in child.children:
                        if isinstance(c, MDCheckbox):
                            c.active = False
            else:
                continue

    def close_dialog(self, obj):
        for child in reversed(sm.get_screen('testDates').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    c.active = False
        self.dialog.dismiss()

    def remove(self):
        for elements in sm.get_screen('testDates').ids.todo_list.children:
            elements.parent.clear_widgets(children=None)

    def add_todo(self, title, description):
        self.ids.todo_list.add_widget(DateCard(title=title, description=description))

    def add_todos(self, title):
        if title != "" and len(title) < 21 and sm.get_screen(
                'add_date').ids.btn.text != 'ADD DEADLINE':
            btntext = sm.get_screen('add_date').ids.btn.text
            x = btntext.split(': ')
            x1 = x[1].split('-')
            today = date.today()
            today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
            dateselected = (x1[2] + '/' + x1[1] + '/' + x1[0])
            datepicked = time.strptime(dateselected, "%d/%m/%Y")
            days = int((time.mktime(datepicked) - time.mktime(today1)) // 86400)
            if days < 0:
                Snackbar(text="Cannot set a deadline for the past :)", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                         font_size="18sp").open()
            else:
                with open("Dates.txt", "r") as f:
                    x = 0
                    lines = f.readlines()
                    lines.append(str(days) + ',' + title + ',' + str(dateselected))
                    print(lines)
                    for line in lines:
                        lines[x] = line.strip('\n')
                        x += 1
                with open("Dates.txt", "w") as f:
                    for line in lines:
                        f.write(line + '\n')
                sm.current = "testDates"
                sm.get_screen("add_date").ids.title.text = ""
                sm.get_screen('add_date').ids.btn.text = "ADD DEADLINE"
        elif title == "":
            Snackbar(text="Title is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif len(title) > 21:
            Snackbar(text="Title too long", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif sm.get_screen('add_date').ids.btn.text == 'ADD DEADLINE':
            Snackbar(text="No date added", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def change_dates(self):
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            for line in reversed(lines):
                y = line.split(',')
                actual_days = time.strptime(str(y[2].strip('\n')), "%d/%m/%Y")
                today = date.today()
                today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                days = int((time.mktime(actual_days) - time.mktime(today1)) // 86400)
                if days < 0:
                    lines.remove(line)
                else:
                    lines[lines.index(line)] = (str(days) + ',' + y[1] + ',' + str(y[2]))
        with open('Dates.txt', 'w') as f:
            x = 0
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            for line in lines:
                f.write(line+'\n')

    def sort_txt_file(self):
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            x = 0
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            lines.sort()
        with open('Dates.txt', 'w') as f:
            for line in lines:
                f.write(line + '\n')

    def on_start(self):
        self.remove()
        self.change_dates()
        self.sort_txt_file()
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.now().year)
        month = str(datetime.now().strftime("%b"))
        day = str(datetime.now().strftime("%d"))
        sm.get_screen('testDates').ids.date.text = f"{days[wd]}, {day} {month} {year}"
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                x = line.split(',')
                title = x[1]
                desc = x[2]
                TestDates.add_todo(sm.get_screen('testDates'), title, desc)

    def datepicker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        sm.get_screen('add_date').ids.btn.text = ('ADD DEADLINE: ' + str(value))


class addDate(Screen):
    def on_start(self):
        self.ids.btn.text = "ADD DEADLINE"

    def datepicker(self):
        TestDates.datepicker(sm.get_screen('testDates'))

    def add_todo(self, title):
        TestDates.add_todos(sm.get_screen('testDates'), title)


class DateCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()

    def on_complete(self, checkbox, value, description, bar, title):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179 / 255, 0, 1
            TestDates.delete(sm.get_screen('testDates'))
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1


class LinkedList:
    def __init__(self, data=None):
        if data is None:
            data = [(None, None)]
        self.title = data[0][0]
        self.desc = data[0][1]
        self.tail = None if (len(data) == 1) else LinkedList(data[1:])

    def insert(self, val):
        new = LinkedList(val)
        new.tail = self.tail
        self.tail = new

    def print_title(self, curr, i):
        x = 0
        while curr:
            if x == i:
                return curr.title
            curr = curr.tail
            x = x + 1

    def print_desc(self, curr, i):
        x = 0
        while curr:
            if x == i:
                return curr.desc
            curr = curr.tail
            x = x + 1


class TodoCard(FakeRectangularElevationBehavior, MDFloatLayout):
    title = StringProperty()
    description = StringProperty()

    def on_complete(self, checkbox, value, description, bar, title):
        if value:
            description.text = f"[s]{description.text}[/s]"
            bar.md_bg_color = 0, 179 / 255, 0, 1
            TodoScreen.delete(sm.get_screen('todo'))
        else:
            remove = ["[s]", "[/s]"]
            for i in remove:
                description.text = description.text.replace(i, "")
                bar.md_bg_color = 1, 170 / 255, 23 / 255, 1


class TodoScreen(Screen):
    dialog = None

    def delete(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete task?",
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Cancel", on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Confirm", on_release=lambda x: self.cancel()
                    ),
                ],
            )
        self.dialog.open()

    def cancel(self):
        for child in reversed(sm.get_screen('todo').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    if c.active:
                        title = child.title
                        desc = child.description
        delete = "DELETE FROM Todolist WHERE Title=? AND Description=?"
        cur.execute(delete, (title, desc))
        con.commit()
        self.close_dialog(self.dialog)
        for elements in sm.get_screen('todo').ids.todo_list.children:
            if elements.ids.title.text == title and elements.ids.description.text == desc:
                elements.parent.remove_widget(elements)
                for child in reversed(sm.get_screen('todo').ids.todo_list.children):
                    for c in child.children:
                        if isinstance(c, MDCheckbox):
                            c.active = False
            else:
                continue

    def close_dialog(self, obj):
        for child in reversed(sm.get_screen('todo').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    c.active = False
        self.dialog.dismiss()

    def remove(self):
        for elements in sm.get_screen('todo').ids.todo_list.children:
            elements.parent.clear_widgets(children=None)

    def add_todo(self, title, description):
        self.ids.todo_list.add_widget(TodoCard(title=title, description=description))

    def add_todos(self, title, description):
        if title != "" and description != "" and len(title) < 21 and len(description) < 61 and sm.get_screen(
                'add_todo').ids.btn.text != 'ADD TASK':
            btntext = sm.get_screen('add_todo').ids.btn.text
            x = btntext.split(': ')
            x1 = x[1].split('-')
            today = date.today()
            today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
            datepicked = time.strptime((x1[2] + '/' + x1[1] + '/' + x1[0]), "%d/%m/%Y")
            days = int((time.mktime(datepicked) - time.mktime(today1)) // 86400)
            if days < 0:
                Snackbar(text="Cannot set a task for the past :)", snackbar_x="10dp", snackbar_y="10dp",
                         size_hint_y=.08,
                         size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                         font_size="18sp").open()
            else:
                insert = ("INSERT INTO Todolist(Title, Description, Days, Date)"
                          "VALUES (?, ?, ?, ?)")
                data = (title, description, days, x[1])
                cur.execute(insert, data)
                con.commit()
                sm.current = "todo"
                sm.get_screen("add_todo").ids.description.text = ""
                sm.get_screen("add_todo").ids.title.text = ""
                sm.get_screen('add_todo').ids.btn.text = "ADD TASK"
        elif title == "":
            Snackbar(text="Title is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif description == "":
            Snackbar(text="Description is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif len(title) > 21:
            Snackbar(text="Title too long", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif len(description) > 61:
            Snackbar(text="Description too long", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        elif sm.get_screen('add_todo').ids.btn.text == 'ADD TASK':
            Snackbar(text="No date added", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def on_start(self):
        today = date.today()
        wd = date.weekday(today)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        year = str(datetime.now().year)
        month = str(datetime.now().strftime("%b"))
        day = str(datetime.now().strftime("%d"))
        self.ids.date.text = f"{days[wd]}, {day} {month} {year}"
        statement = "SELECT Title, Description FROM Todolist ORDER BY Days ASC"
        cur.execute(statement)
        tasks = cur.fetchall()
        for task in tasks:
            TodoScreen.add_todo(sm.get_screen('todo'), task[0], task[1])

    def datepicker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        sm.get_screen('add_todo').ids.btn.text = ('ADD TASK: ' + str(value))


class addTodo(Screen):
    def on_start(self):
        self.ids.btn.text = "ADD TASK"

    def datepicker(self):
        TodoScreen.datepicker(sm.get_screen('todo'))

    def add_todo(self, title, description):
        TodoScreen.add_todos(sm.get_screen('todo'), title, description)


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
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(WeeklyTimetable(name='weeklyTimetable'))
        sm.add_widget(Settings_Screen(name='settings'))
        sm.add_widget(Timers(name='Timer_screen'))
        sm.add_widget(TestDates(name='testDates'))
        sm.add_widget(addDate(name='add_date'))
        sm.add_widget(TodoScreen(name='todo'))
        sm.add_widget(addTodo(name='add_todo'))
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
        statement = "SELECT Email, Password FROM Settings ORDER BY Name ASC"
        cur.execute(statement)
        users = cur.fetchall()
        for user in users:
            if user[0] == id.ids.email.text:
                if user[1] == id.ids.passwd.text:
                    id.ids.email.text = ''
                    id.ids.passwd.text = ''
                    return True
        return False


class WeeklyTimetable(Screen):
    def datatable(self):
        self.data_tables = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.72),
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
                    "Task",
                    "Task",
                    "Task",
                    "Task",
                    "Task",
                    "Task",
                    "Task",
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
    def get_tasks(self):
        statements = "SELECT Title, Description FROM Todolist ORDER BY Days DESC"
        cur.execute(statements)
        t = cur.fetchall()
        tasks = LinkedList()
        for task in t:
            tasks.insert([task])
        return tasks

    def on_row_press_weekday(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        copy2 = quickstart.dates.copy()
        tasks = self.get_tasks()
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
        if current_row.index == 15:
            Task = MDDialog(title=tasks.print_title(tasks, 1), text=tasks.print_desc(tasks, 1))
            Task.open()
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

    def on_row_press_weekend(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        copy2 = quickstart.dates.copy()
        tasks = self.get_tasks()
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
        if current_row.index == 15:
            Task = MDDialog(title=tasks.print_title(tasks, 1), text=tasks.print_desc(tasks, 1))
            Task.open()
        if current_row.index == 17 or current_row.index == 3:
            Revision = MDDialog(title="Revision", text="Make list of subjects and choose i from randon.choice")
            Revision.open()
        if current_row.index == 19:
            hw3d = MDDialog(title="Hw Description", text=str(copy2[2][2]))
            hw3d.open()

    def datatable(self):
        statement = "SELECT Title, Description, Date FROM Todolist"
        cur.execute(statement)
        tasks = cur.fetchall()
        for task in tasks:
            today = date.today()
            x = task[2]
            x1 = x.split('-')
            today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
            datepicked = time.strptime((x1[2] + '/' + x1[1] + '/' + x1[0]), "%d/%m/%Y")
            days = int((time.mktime(datepicked) - time.mktime(today1)) // 86400)
            if days < 0:
                delete = "DELETE FROM Todolist WHERE Title=? AND Description=?"
                cur.execute(delete, (task[0], task[1]))
            else:
                statement = "UPDATE Todolist SET Days=? WHERE Title=? AND Description=?"
                cur.execute(statement, (days, task[0], task[1]))
            con.commit()
        copy = quickstart.dates.copy()
        tasks = self.get_tasks()
        self.weekday = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.28, 0.72),
            column_data=[
                (calendar.day_name[date.today().weekday()], dp(20)),
                ("", dp(55)),
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
                    tasks.print_title(tasks, 1),
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
            size_hint=(0.28, 0.72),
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
                    tasks.print_title(tasks, 1),
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
    pass


class StartScreen(Screen):
    pass


if __name__ == "__main__":
    TouchApp().run()
