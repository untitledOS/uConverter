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
        self.text = QtWidgets.QLabel("Choose a URL:", alignment=QtCore.Qt.AlignTop)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setWindowTitle("YouTube Downloader Deluxe")

        self.button.clicked.connect(self.download)

    @QtCore.Slot()
    def download(self):
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = MyWidget()
    widget.resize(250, 300)
    widget.show()

    sys.exit(app.exec())
