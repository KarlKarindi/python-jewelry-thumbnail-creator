from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton
from PyQt5.QtCore import Qt, QUrl
from src.resizer import resizer
from src.resizer.args import Args
import sys
import os
import numpy as np


def toggle_reflection_removal():
    ARGS.do_reflection_removal = not ARGS.do_reflection_removal


class ListboxWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.resize(600, 600)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            links = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                    links.append(str(url.toLocalFile()))
                else:
                    links.append(str(url.toString()))
            self.addItems(links)
        else:
            event.ignore()


class AppDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 600)
        self.lstBoxView = ListboxWidget(self)
        self.btn = QPushButton("Alusta", self)
        self.btn.setGeometry(850, 400, 200, 50)
        self.btn.clicked.connect(
            lambda: resizer.execute(self.getInputPath(), ARGS))

    def getInputPath(self):
        item = QListWidgetItem(self.lstBoxView.currentItem())
        return item.text()


ARGS = Args()
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
