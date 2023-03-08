import sys
import utils
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import pages.code.main_page_copy
import pages.code.not_a_guide_buy_license

from PySide6 import QtCore
print(QtCore.QCoreApplication.libraryPaths())

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

"""
tasks:
login
display name and type
create room
"""

client = utils.Client(None, None, None)
print(client.username)

app = QApplication(sys.argv)
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

my_form_list = [my_form, my_form2, my_form3, my_form4, my_form5]
my_form_texts_lists = [my_form.heading.text(), my_form2.heading.text(), my_form3.heading.text()]

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
    user_name = client.username
    user_type = client.type
    if user_name is None or user_type is None:
        user_name = "anon"
        user_type = "normal"
    print(user_name, user_type)
    print(text)
    text = text.replace("{name}", user_name)
    text = text.replace("{user_type}", user_type)
    print(text)
    return text
    
def change_window(index):
    sw.setCurrentIndex(index)
    print(index)
    try:
        h = my_form_texts_lists[index]
        print(h)
        h = change_heading_text(h)
        print(h)
        my_form_list[index].heading.setText(h)
    except AttributeError as e:
        print(e)
    except IndexError as e:
        print(e)

my_form.create_new_room_button.clicked.connect(lambda: change_window(1))
my_form.connect_button.clicked.connect(lambda: change_window(2))
my_form.login_button.clicked.connect(lambda: change_window(3))

my_form2.return_button.clicked.connect(lambda: change_window(0))

my_form3.leave_room_button.clicked.connect(lambda: change_window(0))

my_form4.password_field.setEchoMode(QLineEdit.Password)
my_form4.toggle_password.clicked.connect(lambda: toggle_password(my_form4))
my_form4.user_log_in_button.clicked.connect(login)
my_form4.create_new_user_button.clicked.connect(lambda: change_window(4))
my_form4.return_button.clicked.connect(lambda: change_window(0))

my_form5.password_field.setEchoMode(QLineEdit.Password) 
my_form5.user_type_input.clear()
for i in ("normal", "guide"):
    my_form5.user_type_input.addItem(i)
my_form5.toggle_password.clicked.connect(lambda: toggle_password(my_form5))
my_form5.create_user_button.clicked.connect(create_new_user)
my_form5.login_button.clicked.connect(lambda: change_window(3))
my_form5.return_button.clicked.connect(lambda: change_window(0))
    
sw.show()
change_window(0)

