import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import pages.code.main_page_copy
import pages.code.not_a_guide_buy_license

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

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

sw = QStackedWidget()
sw.setFixedSize(551, 728)
sw.addWidget(my_form)
sw.addWidget(my_form2)
sw.addWidget(my_form3)
my_form.create_new_room_button.clicked.connect(lambda: sw.setCurrentIndex(1))
my_form.connect_button.clicked.connect(lambda: sw.setCurrentIndex(2))
my_form3.leave_room_button.clicked.connect(lambda: sw.setCurrentIndex(0))

sw.show()
