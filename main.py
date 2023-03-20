import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

class YTDDMainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.button = QtWidgets.QPushButton("Download")
        self.text = QtWidgets.QLabel("Trapeze YouTube Downloader", alignment=QtCore.Qt.AlignTop)
        
        # User Input
        self.url_input_box = QtWidgets.QLineEdit(self)
        self.url_input_box.setPlaceholderText("Enter a URL...")
        self.open_button = QtWidgets.QPushButton("Open")
        self.quit_button = QtWidgets.QPushButton("Quit")

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setWindowTitle("Trapeze YouTube Downloader")

        self.button.clicked.connect(self.yt_download)

    @QtCore.Slot()
    def yt_download(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(250, 300)
    widget.show()

    sys.exit(app.exec())
