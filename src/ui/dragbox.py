from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QSlider, QSlider
from PyQt5.QtCore import Qt, QUrl
from src.resizer import resizer
from src.resizer.args import Args
import sys
import os
import numpy as np





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
        
        self.paddingSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        self.paddingSlider.setGeometry(800, 100, 200, 50)
        self.paddingSlider.setRange(0, 200)
        self.paddingSlider.setPageStep(20)
        
        self.paddingSlider.valueChanged.connect(self.change_padding)
        
        
        
        self.reflectionCheckBox = QtWidgets.QCheckBox("Eemalda peegeldus", self)
        self.reflectionCheckBox.setGeometry(QtCore.QRect(800, 150, 200, 50))
        self.reflectionCheckBox.setObjectName("checkBoxPeegeldus")
        self.reflectionCheckBox.clicked.connect(self.toggle_reflection_removal)
        self.reflectionCheckBox.setChecked(True)
        
        
        self.startButton = QPushButton("Alusta", self)
        self.startButton.setGeometry(800, 400, 200, 50)
        self.startButton.clicked.connect(
            lambda: self.execute(self.getInputPath(), ARGS))

    def execute(self, input_path, args):
        if len(input_path) <= 0:
            raise Exception("Sisesta sisendkaust")
        else:
            resizer.execute(input_path, args)

    def getInputPath(self):
        item = QListWidgetItem(self.lstBoxView.currentItem())
        return item.text()
    
    def toggle_reflection_removal(self):
        ARGS.do_reflection_removal = not ARGS.do_reflection_removal

    def change_padding(self, value):
        ARGS.padding = value * 10

ARGS = Args()
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
