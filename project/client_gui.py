import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile
import pages.code.main_page_copy
import pages.code.not_a_guide_buy_license

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

app = QApplication(sys.argv)

loader = QUiLoader()

ui_file = QFile("pages/main_page.ui")
ui_file.open(QFile.ReadOnly)
my_form = loader.load(ui_file)
ui_file.close()

ui_file2 = QFile("pages/create_room_page.ui")
ui_file2.open(QFile.ReadOnly)
my_form2 = loader.load(ui_file2)
ui_file2.close()

sw = QStackedWidget()
sw.addWidget(my_form)
sw.addWidget(my_form2)
my_form.create_new_room_button.clicked.connect(lambda: sw.setCurrentIndex(1))

sw.show()
