import sys
import utils
import subprocess 
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit, QMenu, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from pages.code import user_menu
from pages.code import chat_menu
from pages.code import map_menu
import class_broadcast
import class_listener

from PySide6 import QtCore
print(QtCore.QCoreApplication.libraryPaths())

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

"""
tasks:
"""

client = utils.Client(None, None, None)
print(client.username)

class ChangeUsernameDialog(QDialog):
    def __init__(self, ):
        super().__init__()
        self.setWindowTitle("Change Username")

        layout = QVBoxLayout()

        # Create a label and line edit for input
        self.label = QLabel("Enter new username:")
        self.line_edit = QLineEdit()

        # Create a button to accept the input
        self.button = QPushButton("OK")
        self.button.clicked.connect(self.accept)

        # Add widgets to the layout
        layout.addWidget(self.label)
        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        # Set the layout for the dialog
        self.setLayout(layout)

voice_client = None
global_room_code = None

app = QApplication(sys.argv)
with open("pages/style.css", "r") as f:
    app.setStyleSheet(f.read())
app.setWindowIcon(QIcon('icon.png'))

loader = QUiLoader()

main_page = QFile("pages/main_page.ui")
main_page.open(QFile.ReadOnly)
my_form = loader.load(main_page)
main_page.close()
main_page_heading_text = "Hello {name}\nYou are {user_type}"

create_room_page = QFile("pages/create_room_page.ui")
create_room_page.open(QFile.ReadOnly)
my_form2 = loader.load(create_room_page)
create_room_page.close()
create_room_page_heading_text = "Hello {name}"

chat_page = QFile("pages/chat_page.ui")
chat_page.open(QFile.ReadOnly)
my_form3 = loader.load(chat_page)
chat_page.close()
chat_page_heading_text = "Hello, {name}"

login_page = QFile("pages/login_page.ui")
login_page.open(QFile.ReadOnly)
my_form4 = loader.load(login_page)
login_page.close()

create_user_page = QFile("pages/create_new_user.ui")
create_user_page.open(QFile.ReadOnly)
my_form5 = loader.load(create_user_page)
create_user_page.close()

user_menu_page = QFile("pages/user_menu.ui")
user_menu_page.open(QFile.ReadOnly)
my_form6 = loader.load(user_menu_page)
user_menu_page.close()

chat_for_guide_page = QFile("pages/chat_page_for_guide.ui")
chat_for_guide_page.open(QFile.ReadOnly)
my_form7 = loader.load(chat_for_guide_page)
chat_for_guide_page.close()
chat_for_guide_page_heading_text = "Hello, {name}"

my_form_list = [my_form, my_form2, my_form3, my_form7, my_form4, my_form5]
my_form_texts_lists = [my_form.heading.text(), my_form2.heading.text(), my_form3.heading.text(), my_form7.heading.text()]

sw = QStackedWidget()
for i in my_form_list:
    sw.addWidget(i)


def toggle_password(form):
    if form.password_field.echoMode() == QLineEdit.Password:
        form.password_field.setEchoMode(QLineEdit.Normal)
        form.toggle_password.setText("Hide Password")
    else:
        form.password_field.setEchoMode(QLineEdit.Password)
        form.toggle_password.setText("Show Password")


def login():
    # {"password": "123", "email": "check6@gmail.com"}
    mail = my_form4.email_field.text()
    password = my_form4.password_field.text()
    data = {"password": password, "email": mail}
    print(data)
    client.change_user(None, password, mail)
    r = client.send_login()
    print(r)
    if r["code"] == 201:
        change_window(0)


def create_new_user():
    name = my_form5.name_field.text()
    mail = my_form5.email_field.text()
    password = my_form5.password_field.text()
    user_type = my_form5.user_type_input.currentText()
    print(name, mail, password, user_type)
    data = {"username": name, "password": password, "email": mail, "type": user_type}
    print(data)
    client.change_user(None, mail, password)
    r = client.create_user(data)
    print(r)


def change_heading_text(text):
    global voice_client, global_room_code
    try:
        user_name = client.username
        user_type = client.type
        if user_name is None or user_type is None:
            user_name = "anon"
            user_type = "normal"
        print(user_name, user_type)
        text = text.replace("{name}", user_name)
        text = text.replace("{user_type}", user_type)
    except AttributeError as e:
        print(e)
    except IndexError as e:
        print(e)
    try:
        print(global_room_code, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        text = text.replace("{room_code}", str(global_room_code))
    except Exception as e:
        print(e)
    return text
    
def change_window(index):
    sw.setCurrentIndex(index)
    print(index)
    try:
        h = my_form_texts_lists[index]
        h = change_heading_text(h)
        my_form_list[index].heading.setText(h)
    except Exception as e:
        print(e)


def enter_room():
    global voice_client, room_code
    room_code = my_form.room_code_field.text()
    print(room_code)
    change_window(2)
    audio_client = class_listener.AudioClient(room_code, client)
    audio_client.run()
    
    voice_client = audio_client
    

sub_window = None
def open_sub_window():
    global sub_window, voice_client
    if sub_window is None or not sub_window.isVisible():
        sub_window = user_menu.SubWindow(sw, voice_client)
        sub_window.closed.connect(sub_window_closed)
        sub_window.show_fullscreen()


def sub_window_closed():
    global sub_window
    sub_window = None

sub_chat = None
def open_sub_chat():
    global sub_chat, voice_client
    if sub_chat is None or not sub_chat.isVisible():
        sub_chat = chat_menu.ChatSubWindow(sw, voice_client)
        sub_chat.closed.connect(sub_chat_closed)
        sub_chat.show_fullscreen()

        voice_client.update_chat_room(sub_chat)


def sub_chat_closed():
    global sub_chat
    sub_chat = None

sub_map = None
def open_sub_map():
    global sub_map
    if sub_map is None or not sub_map.isVisible():
        sub_map = map_menu.ChatSubWindow(sw)
        sub_map.closed.connect(sub_map_closed)
        sub_map.show_fullscreen()



def sub_map_closed():
    global sub_map
    sub_map = None


def open_room():
    global voice_client, global_room_code
    if client.type == "normal":
        return
    utils.close_room(client.user_data)

    # Create an AudioRecorder object with the client object and parameters
    ip, port1, port2 = utils.get_port_and_ip()
    recorder = class_broadcast.AudioRecorder(client=client, udp_ip=ip, udp_port=51166,
                             host_listener_port=51167)

    # Start recording in the background
    recorder.run()

    voice_client = recorder
    global_room_code = voice_client.room_code
    print(global_room_code, "ggggggggggggggggggggggggggg")
    
    change_window(3)

def change_room_code():
    new_room_code = my_form2.new_code_entry.text()
    utils.request_to_change_room_code(new_room_code, client.user_data)

def ask_to_change_name():
    dialog = ChangeUsernameDialog()
    if dialog.exec() == 1:
        # Retrieve the new username
        new_username = dialog.line_edit.text()
        voice_client.send_change_name(new_username)


def leave_room():
    global voice_client
    voice_client.is_done = True
    change_window(0)
    del voice_client
    voice_client = None

def close_room():
    global voice_client
    voice_client.is_done = True
    voice_client.broadcast("stop".encode())
    utils.close_room(client.user_data)
    change_window(0)
    del voice_client
    voice_client = None
    
clipboard = app.clipboard()

my_form.create_new_room_button.clicked.connect(lambda: change_window(1))
my_form.connect_button.clicked.connect(lambda: enter_room())
my_form.login_button.clicked.connect(lambda: change_window(4))

my_form2.return_button.clicked.connect(lambda: change_window(0))
my_form2.open_room_button.clicked.connect(open_room)
my_form2.request_new_code_button.clicked.connect(change_room_code)

my_form3.leave_room_button.clicked.connect(leave_room)
my_form3.open_chat_button.clicked.connect(open_sub_chat)
my_form3.show_map_button.clicked.connect(open_sub_map)
my_form3.change_name_button.clicked.connect(ask_to_change_name)

my_form4.password_field.setEchoMode(QLineEdit.Password)
my_form4.toggle_password.clicked.connect(lambda: toggle_password(my_form4))
my_form4.user_log_in_button.clicked.connect(login)
my_form4.create_new_user_button.clicked.connect(lambda: change_window(5))
my_form4.return_button.clicked.connect(lambda: change_window(0))

my_form5.password_field.setEchoMode(QLineEdit.Password) 
my_form5.user_type_input.clear()
for i in ("normal", "guide"):
    my_form5.user_type_input.addItem(i)
my_form5.toggle_password.clicked.connect(lambda: toggle_password(my_form5))
my_form5.create_user_button.clicked.connect(create_new_user)
my_form5.login_button.clicked.connect(lambda: change_window(4))
my_form5.return_button.clicked.connect(lambda: change_window(0))

my_form7.show_users_button.clicked.connect(lambda: open_sub_window())
my_form7.open_chat_button.clicked.connect(lambda: open_sub_chat())
my_form7.copy_button.clicked.connect(lambda: clipboard.setText(str(global_room_code)))
my_form7.show_map_button.clicked.connect(lambda: open_sub_map())
my_form7.close_room_button.clicked.connect(close_room)

sw.show()
change_window(0)


