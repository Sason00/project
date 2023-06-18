from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QMenu
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QObject, Signal, QPropertyAnimation, QPoint, QRect, QEasingCurve, QTimer
from PySide6 import QtCore


class SubWindow(QWidget):
    closed = Signal()

    def __init__(self, parent=None, client=None):
        super().__init__(parent)
        
        self.setGeometry(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white; border: 1px solid black; color: black;")

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.close)

        vbox = QVBoxLayout(self)
        vbox.addWidget(close_btn)

        self.list_widget = QListWidget()
        vbox.addWidget(self.list_widget)
        self.list_widget.itemClicked.connect(self.remove_user)
        last_indices = [t[-1] for t in client.clients]
        self.client = client
        print(client.clients)
        if client != None:
            if len(client.clients) !=0:
                self.list_widget.addItems(last_indices)

        # Create the animation object
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)

    def remove_user(self, current_item):
        if current_item is not None:
            selected_item_index = self.list_widget.row(current_item)
            print(selected_item_index)
            self.client.remove_user(selected_item_index)

    def show_fullscreen(self):
        desktop_rect = QGuiApplication.primaryScreen().availableGeometry()
        height = desktop_rect.height() * 3/4
        width = self.parent().width()
        self.setGeometry(0, desktop_rect.height()-height, width, height)

        # Set the start and end positions of the animation
        start_pos = QRect(0, desktop_rect.height(), width, height)
        end_pos = QRect(0, desktop_rect.height()-height, width, height)
        self.animation.setStartValue(start_pos)
        self.animation.setEndValue(end_pos)

        # Start the animation
        self.animation.start()

        self.show()

    def closeEvent(self, event):
        self.closed.emit()
        super().closeEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        button = QPushButton("Open Sub Window")
        button.clicked.connect(self.open_sub_window)

        self.setCentralWidget(button)

        self.sub_window = None

    def open_sub_window(self):
        if self.sub_window is None or not self.sub_window.isVisible():
            self.sub_window = SubWindow(self)
            self.sub_window.closed.connect(self.sub_window_closed)
            self.sub_window.show_fullscreen()

    def sub_window_closed(self):
        self.sub_window = None


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
