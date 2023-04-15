from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QListWidget, QTextEdit, QLineEdit, QSpacerItem, QSizePolicy
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QObject, Signal, QPropertyAnimation, QPoint, QRect, QEasingCurve, QTimer
from PySide6 import QtCore


class ChatSubWindow(QWidget):
    closed = Signal()

    def __init__(self, parent=None, client=None):
        super().__init__(parent)

        if client != None:
            self.client = client
        else:
            self.client = utils.Client(None, None, None)

        self.client = client
        
        self.setGeometry(0, 0, 0, 0)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: white; border: 1px solid black; color: black;")


        # Set up the layout
        self.layout = QVBoxLayout()

        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        self.layout.addWidget(self.close_btn)

        # Add the chat log
        self.chat_log = QTextEdit()
        self.chat_log.setReadOnly(True)
        self.chat_log.setMinimumHeight(200)  # Increase the height of the text box
        self.layout.addWidget(self.chat_log)

        # Add the text input and send button
        self.input_layout = QHBoxLayout()
        self.input_text = QLineEdit()
        self.input_text.setFixedHeight(80)
        self.input_layout.addWidget(self.input_text, 1)  # Add stretch to the text input

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(80)
        self.send_button.setFixedWidth(80)
        self.send_button.clicked.connect(self.send_message)
        self.input_layout.addWidget(self.send_button)
        self.layout.addLayout(self.input_layout)

        # Add some space at the bottom
        spacer_item = QSpacerItem(100, 100, QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.layout.addItem(spacer_item)
        
        self.setLayout(self.layout)


        # Create the animation object
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(500)

    def send_message(self):
        message = self.input_text.text()
        self.chat_log.append(f"You: {message}")
        self.input_text.clear()

        if self.client != None:
            self.client.send_msg(message)

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
            self.sub_window = ChatSubWindow(self)
            self.sub_window.closed.connect(self.sub_window_closed)
            self.sub_window.show_fullscreen()

    def sub_window_closed(self):
        self.sub_window = None


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
