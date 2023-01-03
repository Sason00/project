import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

import pages.code.main_page_copy
import pages.code.not_a_guide_buy_license

# C:\Users\Ariel\AppData\Roaming\Python\Python311\Scripts\pyside6-uic.exe

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create a QStackedWidget and add the screens to it
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(pages.code.main_page_copy.Ui_Form())
        self.stacked_widget.addWidget(pages.code.not_a_guide_buy_license.Ui_MainWindow())

        # Set the main window's central widget to the stacked widget
        self.setCentralWidget(self.stacked_widget)

    def switch_to_main_page(self):
        # Switch to the main page
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(0))

    def switch_to_not_a_guide_buy_license(self):
        # Switch to the "not a guide, buy a license" page
        self.stacked_widget.setCurrentWidget(self.stacked_widget.widget(1))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
