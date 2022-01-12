from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from datetime import date, datetime, timedelta
from kivymd.uix.behaviors import FakeRectangularElevationBehavior
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.picker import MDDatePicker
import calendar
import sqlite3
import random
import quickstart
import time

con = sqlite3.connect('ReviseTime.db')
cur = con.cursor()
Builder.load_file("kivy.kv")
Config.set('graphics', 'resizeable', 1)
Config.set('graphics', 'position', "auto")
Config.write()
sm = ScreenManager()


def change_volume():
    cur.execute('SELECT Sound FROM Settings')
    volume = cur.fetchone()
    if volume is None:
        return 1
    else:
        Sound.volume = float(volume[0])
        return Sound.volume


class Settings2(BoxLayout):
    pass


class Settings3(BoxLayout):
    cur.execute("SELECT H1, H2, H3, S1, S2, S3 FROM Subjects")
    subjects = cur.fetchone()
    if subjects is None:
        pass
    else:
        H1 = subjects[0]
        H2 = subjects[1]
        H3 = subjects[2]
        S1 = subjects[3]
        S2 = subjects[4]
        S3 = subjects[5]


class Settings_Screen(Screen):
    val = (change_volume() * 10)
    dialog = None
    create = None

    def on_start(self):
        sm.get_screen('settings').ids.Spinner.text = 'Settings'

    def SQLite_volume(self):
        # update volume in SQLite table
        cur.execute('UPDATE Settings SET Sound=?', [str(sm.get_screen('settings').ids.slider.value / 10)])
        con.commit()
        # Change volume in application
        change_volume()

    def open(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Personal Information for authentication:",
                size_hint=[0.5, None],
                auto_dismiss=False,
                type="custom",
                content_cls=Settings2(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="Check", on_release=self.check
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        self.dialog.content_cls.ids.email.text = ''
        self.dialog.content_cls.ids.password.text = ''

    def check(self, obj):
        statement = "SELECT Email, Password " \
                    "FROM Settings ORDER BY Name ASC"
        cur.execute(statement)
        users = cur.fetchall()
        # Search through users SQLite data table
        for user in users:
            if user[0] == self.dialog.content_cls.ids.email.text:
                if user[1] == self.dialog.content_cls.ids.password.text:
                    self.dialog.dismiss()
                    self.dialog.content_cls.ids.email.text = ''
                    self.dialog.content_cls.ids.password.text = ''
                    self.change2()

    def change2(self):
        if not self.create:
            self.create = MDDialog(
                title="Only enter information you want changed:",
                size_hint=[0.5, None],
                auto_dismiss=False,
                type="custom",
                content_cls=Settings3(),
                buttons=[
                    MDFlatButton(
                        text="Close", on_release=self.close
                    ),
                    MDFlatButton(
                        text="Change information", on_release=self.change_info
                    ),
                ],
            )
        self.create.open()

    def close(self, obj):
        self.create.dismiss()
        self.create.content_cls.ids.HL1.text = ''
        self.create.content_cls.ids.HL2.text = ''
        self.create.content_cls.ids.HL3.text = ''
        self.create.content_cls.ids.SL1.text = ''
        self.create.content_cls.ids.SL2.text = ''
        self.create.content_cls.ids.SL3.text = ''

    def change_info(self, obj):
        self.create.dismiss()
        cur.execute("SELECT H1, H2, H3, S1, S2, S3 FROM Subjects")
        subjects = cur.fetchone()
        cur.execute("SELECT Name, Email, Password FROM Settings")
        stuff = cur.fetchone()
        if stuff is None:
            pass
        else:
            H1 = subjects[0]
            H2 = subjects[1]
            H3 = subjects[2]
            S1 = subjects[3]
            S2 = subjects[4]
            S3 = subjects[5]
            email = stuff[1]
            password = stuff[2]
            name = stuff[0]
        if self.create.content_cls.ids.HL1.text == '':
            pass
        else:
            H1 = self.create.content_cls.ids.HL1.text
        if self.create.content_cls.ids.HL2.text == '':
            pass
        else:
            H2 = self.create.content_cls.ids.HL2.text
        if self.create.content_cls.ids.HL3.text == '':
            pass
        else:
            H3 = self.create.content_cls.ids.HL3.text
        if self.create.content_cls.ids.SL1.text == '':
            pass
        else:
            S1 = self.create.content_cls.ids.SL1.text
        if self.create.content_cls.ids.SL2.text == '':
            pass
        else:
            S2 = self.create.content_cls.ids.SL2.text
        if self.create.content_cls.ids.SL3.text == '':
            pass
        else:
            S3 = self.create.content_cls.ids.SL3.text
        if self.create.content_cls.ids.email.text == '':
            pass
        else:
            email = self.create.content_cls.ids.email.text
        if self.create.content_cls.ids.password.text == '':
            pass
        else:
            password = self.create.content_cls.ids.password.text
        if self.create.content_cls.ids.name.text == '':
            pass
        else:
            name = self.create.content_cls.ids.name.text
        self.create.content_cls.ids.HL1.text = ''
        self.create.content_cls.ids.HL2.text = ''
        self.create.content_cls.ids.HL3.text = ''
        self.create.content_cls.ids.SL1.text = ''
        self.create.content_cls.ids.SL2.text = ''
        self.create.content_cls.ids.SL3.text = ''
        self.create.content_cls.ids.name.text = ''
        self.create.content_cls.ids.email.text = ''
        self.create.content_cls.ids.password.text = ''
        cur.execute("UPDATE Subjects SET H1=?, H2=?, H3=?, S1=?, S2=?, S3=?", [H1, H2, H3, S1, S2, S3])
        cur.execute("UPDATE Settings SET Email=?, Password=?, Name=?", [email, password, name])
        con.commit()


class Timers(Screen):
    dialog = None

    def __init__(self, **kwargs):
        super(Timers, self).__init__(**kwargs)
        arg = '60'
        countdown = int(arg.split("m")[0])
        self.sound = SoundLoader.load('bell.wav')
        self.delta = datetime.now() + timedelta(0, 60 * countdown)
        self.update()

    def on_start(self):
        sm.get_screen('Timer_screen').ids.Spinner.text = 'Timer'
        if self.running:
            pass
        else:
            if not self.dialog:
                self.dialog = MDDialog(
                    title="Timer length",
                    size_hint=(0.5, 0.2),
                    type='custom',
                    auto_dismiss=False,
                    buttons=[MDFlatButton(text="Start 60 minutes Timer", on_release=lambda x: self.close('60mins')),
                             MDFlatButton(text="Start 30 minutes Timer", on_release=lambda x: self.close('30mins')),
                             MDFlatButton(text="Start 15 minutes Timer", on_release=lambda x: self.close('15mins')),
                             MDFlatButton(text="Close", on_release=lambda x: self.cancel())],
                )
            self.dialog.open()

    minutes = StringProperty()
    seconds = StringProperty()
    running = BooleanProperty(False)

    def cancel(self):
        self.dialog.dismiss()

    def close(self, arg):
        self.dialog.dismiss()
        countdown = int(arg.split("m")[0])
        self.delta = datetime.now() + timedelta(0, 60 * countdown)
        self.update()
        self.start()

    def start(self):
        if not self.running:
            self.running = True
            Clock.schedule_interval(self.update, 0.05)

    def stop(self):
        if self.running:
            self.running = False
            Clock.unschedule(self.update)

    def update(self, *kwargs):
        delta = self.delta - datetime.now()
        self.minutes, seconds = str(delta).split(":")[1:]
        self.seconds = seconds[:5]

        if int(self.minutes) == 0:
            if int(self.seconds.split(".")[0]) == 0:
                try:
                    if int(self.seconds.split(".")[1]) < 20:
                        self.seconds = "00.00"
                        self.sound.play()
                        self.stop()
                        sm.current = 'Timer_screen'
                except IndexError:
                    pass

    def toggle(self):
        if self.running:
            self.stop()
            self.on_start()
        else:
            self.start()


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

    # Remove from text file
    def cancel(self):
        # Remove deadline from screen
        for child in reversed(sm.get_screen('testDates').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    if c.active:
                        title = child.title
                        desc = child.description
        # Open text file in read-only mode
        with open('Dates.txt', 'r') as f:
            # Get all lines in txt file as a list
            lines = f.readlines()
            # Search all the lines to fine a line with the same title, description and days till deadline as the
            # checkbox selected
            for line in lines:
                desc_days = time.strptime(str(desc).strip('\n'), "%d/%m/%Y")
                today = date.today()
                today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                days = int((time.mktime(desc_days) - time.mktime(today1)) // 86400)
                # If correct line is found remove line from list of lines
                if line.strip('\n') == str(days) + ',' + str(title) + ',' + str(desc).strip('\n'):
                    lines.remove(line)
        # Reopen text file in write mode
        with open('Dates.txt', 'w') as f:
            x = 0
            # Loop through all lines in in list of lines and add them into the text file
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            for line in lines:
                f.write(line + '\n')
        self.close_dialog(self.dialog)
        # Search through all elements in screen find selected checkbox and remove task from screen
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
                # Open text file in read-only mode
                with open("Dates.txt", "r") as f:
                    x = 0
                    # Get lines in text file as a list
                    lines = f.readlines()
                    # Add new deadline into the list
                    lines.append(str(days) + ',' + title + ',' + str(dateselected))
                    for line in lines:
                        lines[x] = line.strip('\n')
                        x += 1
                # reopen text file in write mode
                with open("Dates.txt", "w") as f:
                    # Loop through all lines in list of lines and add them into the text file
                    for line in lines:
                        f.write(line + '\n')
                sm.current = "testDates"
                sm.get_screen("add_date").ids.title.text = ""
                sm.get_screen('add_date').ids.btn.text = "ADD DEADLINE"
        # If no title is given for task display a brief message at the bottom of the screen reminding them
        # that they need to add a title
        elif title == "":
            Snackbar(text="Title is missing", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        # If title for task is too long display a brief message at the bottom of the screen reminding them that
        # the title is too long
        elif len(title) > 21:
            Snackbar(text="Title too long", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()
        # If user has not added a due date for the deadline display a brief message at the bottom of
        # the screen reminding them that they need to add a date
        elif sm.get_screen('add_date').ids.btn.text == 'ADD DEADLINE':
            Snackbar(text="No date added", snackbar_x="10dp", snackbar_y="10dp", size_hint_y=.08,
                     size_hint_x=(Window.width - (dp(10) * 2)) / Window.width,
                     bg_color=(1, 170 / 255, 23 / 255, 1),
                     font_size="18sp").open()

    def change_dates(self):
        # Open text file in read-only mode
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            # Loop through the list in reversed order
            for line in reversed(lines):
                y = line.split(',')
                actual_days = time.strptime(str(y[2].strip('\n')), "%d/%m/%Y")
                today = date.today()
                today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
                days = int((time.mktime(actual_days) - time.mktime(today1)) // 86400)
                # If deadline has passed remove from list
                if days < 0:
                    lines.remove(line)
                # Since days till deadline changes everyday update list to give correct number of days till deadline
                else:
                    lines[lines.index(line)] = (str(days) + ',' + y[1] + ',' + str(y[2]))
        # Open text file in write mode
        with open('Dates.txt', 'w') as f:
            x = 0
            # Write in new list with correct / updated dates with past deadlines removed into the test file
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            for line in lines:
                f.write(line + '\n')

    # Sort deadlines in text file in ascending order based on days till deadline
    def sort_txt_file(self):
        # Open text file in read-only mode
        with open('Dates.txt', 'r') as f:
            lines = f.readlines()
            x = 0
            for line in lines:
                lines[x] = line.strip('\n')
                x += 1
            # Sort list
            lines.sort()
        # Reopen text file in write mode
        with open('Dates.txt', 'w') as f:
            # Loop through all lines in ordered list of lines and add them into the text file
            for line in lines:
                f.write(line + '\n')

    def on_start(self):
        sm.get_screen('testDates').ids.Spinner.text = 'Input Test Dates'
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
        # Loop through linked list while
        # there are still elements in the list
        while curr:
            # If at index specified
            if x == i:
                # Return title of task at
                # that point in the linked list
                return curr.title
            curr = curr.tail
            x = x + 1

    def print_desc(self, curr, i):
        x = 0
        # Loop through linked list while
        # there are still elements in the list
        while curr:
            # If at index specified
            if x == i:
                # Return description of task at
                # that point in the linked list
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
        # Search through all elements in to do list screen
        for child in reversed(sm.get_screen('todo').ids.todo_list.children):
            for c in child.children:
                if isinstance(c, MDCheckbox):
                    # If checkbox selected is found store title and description
                    if c.active:
                        title = child.title
                        desc = child.description
        # Delete task from SQLite data table
        delete = "DELETE FROM Todolist WHERE Title=? AND Description=?"
        cur.execute(delete, (title, desc))
        # Save changes to the database
        con.commit()
        # Close popup
        self.close_dialog(self.dialog)
        # Search through all elements in screen find selected checkbox and remove task from screen
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
        # Show date on screen
        self.ids.date.text = f"{days[wd]}, {day} {month} {year}"
        # Sort tasks in SQLite data table in ascending order of days till deadline
        statement = "SELECT Title, Description FROM Todolist ORDER BY Days ASC"
        cur.execute(statement)
        # Get list of dates matching the select query above
        tasks = cur.fetchall()
        # Add tasks to screen
        for task in tasks:
            TodoScreen.add_todo(sm.get_screen('todo'), task[0], task[1])

    def datepicker(self):
        # Create a calender from which
        # user can select task deadline
        date_dialog = MDDatePicker()
        # When date is selected run
        # on_save() function
        date_dialog.bind(on_save=
                         self.on_save)
        # Open MDDatePicker
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
        self.theme_cls.primary_palette = "Orange"  # "Purple", "Red"
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
        today = date.today()
        today1 = today.strftime("%d/%m/20%y")
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
            IA = random.choice(subjects) + ',' + today1
            Revision1 = random.choice(subjects) + ',' + today1
            Revision2 = random.choice(subjects) + ',' + today1
            self.create.content_cls.ids.error.text = ""
            # Insert users name, email and password into the data table when they sign up

            cur.execute("UPDATE Settings SET Name=?, Email=?, Password=?, Sound=?, IA=?, Revision1=?, Revision2=?",
                        [self.dialog.content_cls.ids.forename.text, self.dialog.content_cls.ids.email.text,
                         self.dialog.content_cls.ids.password.text, '1', IA, Revision1, Revision2])
            # Insert users subjects to the data table when they sign up
            insert = ("INSERT INTO Subjects(H1, H2, H3, S1, S2, S3)"
                      "VALUES (?, ?, ?, ?, ?, ?)")
            data = (self.create.content_cls.ids.HL1.text, self.create.content_cls.ids.HL2.text,
                    self.create.content_cls.ids.HL3.text, self.create.content_cls.ids.SL1.text,
                    self.create.content_cls.ids.SL2.text, self.create.content_cls.ids.SL3.text)
            cur.execute(insert, data)
            # Commit/save changes to the database
            con.commit()
            self.create.dismiss()
            sm.current = 'menu'
            id = self.root.get_screen('start')
            id.ids.email.text = ''
            id.ids.passwd.text = ''

    def previous_page(self, obj):
        self.create.dismiss()
        self.signup()

    def signin(self, obj):
        id = self.root.get_screen('start')
        statement = "SELECT Email, Password " \
                    "FROM Settings ORDER BY Name ASC"
        cur.execute(statement)
        users = cur.fetchall()
        # Search through users SQLite data table
        for user in users:
            # If email and password user inputted is in
            # the SQLite data table go to main menu
            if user[0] == id.ids.email.text:
                if user[1] == id.ids.passwd.text:
                    id.ids.email.text = ''
                    id.ids.passwd.text = ''
                    return True
        Snackbar(text="Email or password is incorrect", snackbar_x="10dp", snackbar_y="10dp",
                 size_hint_y=.08,
                 size_hint_x=(Window.width - (dp(10) * 2)) / Window.width, bg_color=(1, 170 / 255, 23 / 255, 1),
                 font_size="18sp").open()
        return False


class WeeklyTimetable(Screen):
    def datatable(self):
        sm.get_screen('weeklyTimetable').ids.Spinner.text = 'Weekly Timetable'
        self.data_tables = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.9, 0.72),
            column_data=[
                ("", dp(20)),
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
    def check_IA(self):
        today = date.today().strftime("%d/%m/20%y")
        cur.execute('SELECT IA FROM Settings')
        x = cur.fetchone()
        y = x[0].split(',')
        if y[1] == today:
            IA = y[0]
            return IA
        else:
            cur.execute('SELECT H1, H2, H3, S1, S2, S3 FROM Subjects')
            subjects = cur.fetchone()
            IA = random.choice(subjects)
            cur.execute('UPDATE Settings SET IA=?', ((IA + ',' + today),))
            return IA

    def check_R1(self):
        today = date.today().strftime("%d/%m/20%y")
        cur.execute('SELECT Revision1 FROM Settings')
        x = cur.fetchone()
        y = x[0].split(',')
        if y[1] == today:
            IA = y[0]
            return IA
        else:
            cur.execute('SELECT H1, H2, H3, S1, S2, S3 FROM Subjects')
            subjects = cur.fetchone()
            IA = random.choice(subjects)
            cur.execute('UPDATE Settings SET Revision1=?', ((IA + ',' + today),))
            return IA

    def check_R2(self):
        today = date.today().strftime("%d/%m/20%y")
        cur.execute('SELECT Revision2 FROM Settings')
        x = cur.fetchone()
        y = x[0].split(',')
        if y[1] == today:
            IA = y[0]
            return IA
        else:
            cur.execute('SELECT H1, H2, H3, S1, S2, S3 FROM Subjects')
            subjects = cur.fetchone()
            IA = random.choice(subjects)
            cur.execute('UPDATE Settings SET Revision2=?', ((IA + ',' + today),))
            return IA

    # Retrieve tasks from SQLite database
    def get_tasks(self):
        # Get title and description for tasks in order of number of days till deadline
        statements = "SELECT Title, Description FROM Todolist ORDER BY Days DESC"
        cur.execute(statements)
        t = cur.fetchall()
        tasks = LinkedList()
        for task in t:
            # insert tasks into linked list
            tasks.insert([task])
        return tasks

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
            IA = MDDialog(title="IA", text=self.check_IA())
            IA.open()
        if current_row.index == 15:
            # Searches through the linked list using index given to find title and description of
            # task
            if tasks.print_title(tasks, 1) is None:
                Task = MDDialog(title="Take a break", text="No tasks currently available")
            else:
                Task = MDDialog(title=tasks.print_title(tasks, 1), text=tasks.print_desc(tasks, 1))
            Task.open()
        if current_row.index == 17:
            Revision = MDDialog(title="Revision", text=self.check_R2())
            Revision.open()
        if current_row.index == 3:
            Revision = MDDialog(title="Revision", text=self.check_R1())
            Revision.open()
        if current_row.index == 19:
            # Searches through the nested list using index given to find description of homework
            # task
            hw3d = MDDialog(title="Hw Description", text=str(copy2[2][2]))
            hw3d.open()

    def on_row_press_weekday(self, instance_table, current_row):
        '''Called when a table row is clicked.'''
        copy2 = quickstart.dates.copy()
        tasks = self.get_tasks()
        # Create popup depending on what row of the table is clicked
        # Tell user to take a break at this time
        if current_row.index == 7:
            breaktime = MDDialog(title="BreakTime", text="Take a break! :)")
            breaktime.open()
        # Tell user to work on their EE
        if current_row.index == 9:
            EE = MDDialog(title="EE", text="Time to do your EE")
            EE.open()
        # Show description of task from Google Classroom
        if current_row.index == 11:
            hw1d = MDDialog(title="Hw Description", text=str(copy2[0][2]))
            hw1d.open()
        # Tell user to work on a randomly selected IA
        if current_row.index == 13:
            IA = MDDialog(title="IA", text=self.check_IA())
            IA.open()
        # Searches through the linked list using index given to find title and description of
        # task
        if current_row.index == 15:
            if tasks.print_title(tasks, 1) is None:
                Task = MDDialog(title="Take a break", text="No tasks currently available")
            else:
                Task = MDDialog(title=tasks.print_title(tasks, 1), text=tasks.print_desc(tasks, 1))
            Task.open()
        # Subject revision
        if current_row.index == 17:
            Revision = MDDialog(title="Revision", text=self.check_R1())
            Revision.open()
        # Show description of task from Google Classroom
        if current_row.index == 19:
            # open a popup when row is clicked to show homework description from nested list
            # Searches through the nested list using index given to find description of homework
            hw3d = MDDialog(title="Hw Description", text=str(copy2[1][2]))
            hw3d.open()
        # Motivational quote
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

    def datatable(self):
        sm.get_screen('menu').ids.Spinner.text = 'Main Menu'
        statement = "SELECT Title, Description, Date FROM Todolist"
        cur.execute(statement)
        tasks = cur.fetchall()
        for task in tasks:
            today = date.today()
            x = task[2]
            x1 = x.split('-')
            # Convert today's date and task due date to a usable format
            today1 = time.strptime(today.strftime("%d/%m/20%y"), "%d/%m/%Y")
            datepicked = time.strptime((x1[2] + '/' + x1[1] + '/' + x1[0]), "%d/%m/%Y")
            # Subtract current date from homework date to find time between dates in seconds
            # then divide by the number of seconds in a day to find the number of days between
            # now and the homework due date
            days = int((time.mktime(datepicked) - time.mktime(today1)) // 86400)
            if days < 0:
                # Delete task from data table if deadline has passed
                delete = "DELETE FROM Todolist WHERE Title=? AND Description=?"
                cur.execute(delete, (task[0], task[1]))
            else:
                # Update task with new number of days till deadline if it has chaged
                statement = "UPDATE Todolist SET Days=? WHERE Title=? AND Description=?"
                cur.execute(statement, (days, task[0], task[1]))
            con.commit()
        # create a copy of nested list
        copy = quickstart.dates.copy()
        tasks = self.get_tasks()
        # Create table of data
        self.weekday = MDDataTable(
            elevation=2,
            rows_num=20,
            background_color=[1.0, 1.0, 1.0, 1.0],
            # Position of table on the screen
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.28, 0.72),
            column_data=[
                (calendar.day_name[date.today().weekday()], dp(20)),
                ("", dp(55))
            ],
            row_data=[
                ("1 pm", "School"),
                ("2 pm", "School"),
                ("3 pm", "School"),
                ("4 pm", "Break"),
                ("5 pm", "EE"),
                ("6 pm", str(copy[0][1])),
                ("7 pm", "IA"),
                ("8 pm", tasks.print_title(tasks, 1)),
                ("9 pm", "Revision"),
                ("10 pm", str(copy[2][1]))
            ]
        )
        copy = quickstart.dates.copy()
        self.weekend = MDDataTable(
            rows_num=20,
            elevation=2,
            background_color=[1.0, 1.0, 1.0, 1.0],
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            size_hint=(0.28, 0.72),
            column_data=[
                ('', dp(20)),
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


class StartScreen(Screen):
    pass


if __name__ == "__main__":
    change_volume()
    TouchApp().run()
