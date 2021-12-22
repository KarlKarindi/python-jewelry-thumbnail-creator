from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QPushButton, QSlider, QSlider, QHBoxLayout, QLabel
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
            print(links)
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

        self.paddingLabel = QLabel('0', self)
        # This sets the initial slider label value
        self.paddingLabel.setText(str(10))
        self.paddingLabel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.paddingLabel.setMinimumWidth(80)
        self.paddingLabel.setGeometry(620, 100, 200, 50)

        self.paddingSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        # This sets the initial slider value
        self.paddingSlider.setSliderPosition(100)
        self.paddingSlider.setGeometry(800, 100, 200, 50)
        self.paddingSlider.setRange(0, 200)
        self.paddingSlider.setPageStep(20)
        self.paddingSlider.valueChanged.connect(self.change_padding)
        self.paddingSlider.setFocusPolicy(Qt.NoFocus)

        self.reflectionCheckBox = QtWidgets.QCheckBox(
            "Eemalda peegeldus", self)
        self.reflectionCheckBox.setGeometry(QtCore.QRect(800, 180, 200, 50))
        self.reflectionCheckBox.setObjectName("checkBoxPeegeldus")
        self.reflectionCheckBox.clicked.connect(self.toggle_reflection_removal)
        self.reflectionCheckBox.setChecked(True)

        self.startButton = QPushButton("Alusta", self)
        self.startButton.setGeometry(800, 400, 200, 50)
        self.startButton.clicked.connect(
            lambda: self.handle_start_pressed(self.getInputDirs(), ARGS))

    def handle_start_pressed(self, input_dirs, args):
        if len(input_dirs) <= 0:
            raise Exception("Sisesta sisendkaust")

        data, args = resizer.setup(input_dirs, args)
        for task in data:
            input_dir = task[0]
            output_dir = task[1]
            img_file_names = task[2]
            for ifn in img_file_names:
                img_abspath = input_dir + ifn
                save_loc = output_dir + ifn
                
                result = resizer.resize_img(img_abspath, save_loc, args)
                print(result)

    def getInputDirs(self):
        lbw = self.lstBoxView
        return [QListWidgetItem(lbw.item(index)).text() for index in range(lbw.count())]

    def toggle_reflection_removal(self):
        ARGS.do_reflection_removal = not ARGS.do_reflection_removal

    def change_padding(self, value):
        self.paddingLabel.setText(str(value // 10))
        ARGS.padding = value * 10


ARGS = Args()
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
