from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont, QColor
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

        self.setFixedSize(1000, 600)

        self.lstBoxView = ListboxWidget(self)

        self.paddingLabel = QLabel('0', self)
        # This sets the initial slider label value
        self.paddingLabel.setText("Lisataust: " + str(10))
        self.paddingLabel.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.paddingLabel.setMinimumWidth(60)
        self.paddingLabel.setGeometry(590, 50, 200, 50)

        self.paddingSlider = QtWidgets.QSlider(Qt.Horizontal, self)
        # This sets the initial slider value
        self.paddingSlider.setSliderPosition(100)
        self.paddingSlider.setGeometry(750, 50, 200, 50)
        self.paddingSlider.setRange(0, 200)
        self.paddingSlider.setPageStep(20)
        self.paddingSlider.valueChanged.connect(self.change_padding)
        self.paddingSlider.setFocusPolicy(Qt.NoFocus)
        
        self.reflectionCheckBox = QtWidgets.QCheckBox(
            "Eemalda peegeldus", self)
        self.reflectionCheckBox.setGeometry(QtCore.QRect(650, 130, 200, 50))
        self.reflectionCheckBox.setObjectName("checkBoxPeegeldus")
        self.reflectionCheckBox.clicked.connect(self.toggle_reflection_removal)
        self.reflectionCheckBox.setChecked(True)
        


        self.status = QLabel('← Tiri väljale kaust/kaustad', self)
        self.status.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.status.setMinimumWidth(400)
        self.status.setMaximumWidth(400)
        self.status.setFont(QFont("Arial", 14))
        self.status.setGeometry(650, 350, 200, 50)
        self.status.resize(400, 30)

        self.taskProgressLabel = QLabel('Töödeldud kaustade arv: 0/0', self)
        self.taskProgressLabel.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.taskProgressLabel.setMinimumWidth(400)
        self.taskProgressLabel.setMaximumWidth(400)
        self.taskProgressLabel.resize(400, 30)
        self.taskProgressLabel.setGeometry(650, 390, 200, 50)

        self.taskResizeProgressLabel = QLabel('Kaustas töödeldud piltide arv: 0/0', self)
        self.taskResizeProgressLabel.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter)
        self.taskResizeProgressLabel.setMinimumWidth(400)
        self.taskResizeProgressLabel.setMaximumWidth(400)
        self.taskResizeProgressLabel.resize(400, 30)
        self.taskResizeProgressLabel.setGeometry(650, 420, 200, 50)
        
        self.totalResizeProgressLabel = QLabel('Töödeldud piltide arv kokku: 0/0', self)
        self.totalResizeProgressLabel.setAlignment(
            Qt.AlignLeft | Qt.AlignVCenter)
        self.totalResizeProgressLabel.setMinimumWidth(400)
        self.totalResizeProgressLabel.setMaximumWidth(400)
        self.totalResizeProgressLabel.resize(400, 30)
        self.totalResizeProgressLabel.setGeometry(650, 450, 200, 50)

        self.startButton = QPushButton("Alusta", self)
        self.startButton.setGeometry(650, 500, 200, 50)
        self.startButton.clicked.connect(
            lambda: self.handle_start_pressed(self.getInputDirs(), ARGS))

    def handle_start_pressed(self, input_dirs, args):
        if len(input_dirs) <= 0:
            self.status.setText("Sisendkausta pole sisestatud!")
            return

        self.status.setText("Töötlen pilte...")
        
        data, args, total_picture_count = resizer.setup(input_dirs, args)
        total_resizes_done = 0

        for i, task in enumerate(data):
            input_dir = task[0]
            output_dir = task[1]
            img_file_names = task[2]
            len_img_file_names = len(img_file_names)
            
            pretty_input_dir = input_dir.split("/")[-2]
            self.taskProgressLabel.setText("Töödeldud kaustade arv: " + str(i + 1) + "/" + str(len(data)) + " ("+ pretty_input_dir +")")
            
            for j, ifn in enumerate(img_file_names):
                img_abspath = input_dir + ifn
                save_loc = output_dir + ifn

                result = resizer.resize_img(img_abspath, save_loc, args)
                total_resizes_done += 1
                self.taskResizeProgressLabel.setText(
                    "Kaustas töödeldud piltide arv: " + str(j + 1) + "/" + str(len_img_file_names))
                
                
                self.totalResizeProgressLabel.setText("Töödeldud piltide arv kokku: " + str(total_resizes_done) + "/" + str(total_picture_count))
                app.processEvents()
                
        self.status.setText("Piltide töötlus lõpetatud")

    def getInputDirs(self):
        lbw = self.lstBoxView
        return [QListWidgetItem(lbw.item(index)).text() for index in range(lbw.count())]

    def toggle_reflection_removal(self):
        ARGS.do_reflection_removal = not ARGS.do_reflection_removal

    def change_padding(self, value):
        self.paddingLabel.setText("Lisataust: " + str(value // 10))
        ARGS.padding = value * 10


ARGS = Args()
app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
