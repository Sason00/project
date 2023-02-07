import sys
import utils
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QLineEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import pages.code.main_page_copy
import pages.code.not_a_guide_buy_license

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

"""
tasks:
login
display name and type
create room
"""

app = QApplication(sys.argv)

loader = QUiLoader()

main_page = QFile("pages/main_page.ui")
main_page.open(QFile.ReadOnly)
my_form = loader.load(main_page)
main_page.close()

create_room_page = QFile("pages/create_room_page.ui")
create_room_page.open(QFile.ReadOnly)
my_form2 = loader.load(create_room_page)
create_room_page.close()

chat_page = QFile("pages/chat_page.ui")
chat_page.open(QFile.ReadOnly)
my_form3 = loader.load(chat_page)
chat_page.close()

login_page = QFile("pages/login_page.ui")
login_page.open(QFile.ReadOnly)
my_form4 = loader.load(login_page)
login_page.close()

sw = QStackedWidget()
sw.setFixedSize(551, 728)
sw.addWidget(my_form)
sw.addWidget(my_form2)
sw.addWidget(my_form3)
sw.addWidget(my_form4)


def toggle_password():
    if my_form4.password_field.echoMode() == QLineEdit.Password:
        my_form4.password_field.setEchoMode(QLineEdit.Normal)
        my_form4.toggle_password.setText("Hide Password")
    else:
        my_form4.password_field.setEchoMode(QLineEdit.Password)
        my_form4.toggle_password.setText("Show Password")


def login():
    # {"password": "123", "email": "check6@gmail.com"}
    mail = my_form4.email_field.text()
    password = my_form4.password_field.text()
    data = {"password": password, "email": mail}
    r = utils.send_login(data)
    print(r)
    


my_form.create_new_room_button.clicked.connect(lambda: sw.setCurrentIndex(1))
my_form.connect_button.clicked.connect(lambda: sw.setCurrentIndex(2))
my_form.login_button.clicked.connect(lambda: sw.setCurrentIndex(3))

my_form3.leave_room_button.clicked.connect(lambda: sw.setCurrentIndex(0))

my_form4.password_field.setEchoMode(QLineEdit.Password)
my_form4.toggle_password.clicked.connect(toggle_password)
my_form4.user_log_in_button.clicked.connect(login)


sw.show()
