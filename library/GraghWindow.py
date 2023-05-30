from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt, QEvent

import csv
import shutil
import os

from library.Label import MyLabel


class Graph(QLabel):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap("../images/cat.jpg"))
        self.setFixedSize(QSize(500, 500))
        self.setAlignment(Qt.AlignCenter)


class Button(QPushButton):
    def __init__(self, text, stylesheet):
        super().__init__(text)
        self.set_style(stylesheet)

    def set_style(self, stylesheet):
        stylesheet += '''
                border-radius: 10px;
                padding: 10px;
                min-height: 32px;
                max-width: 250px;

                font-family: 'Inter';
                font-style: normal;
                font-weight: 700;
                font-size: 20px;
                line-height: 24px;
        '''
        self.setStyleSheet(stylesheet)


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = list()
        self.stylesheet_red = '''
                color: white;
                background-color: #F03C3C;
                border: 2px solid transparent;
        '''
        self.stylesheet_grey = '''
                color: #6A6E77;
                background-color: #EBEEF5;
        '''

        main_layout = QVBoxLayout()
        self.image_label = MyLabel("NAME")
        self.image_label.set_text("Some image")
        main_layout.addWidget(self.image_label)

        self.graph = Graph()
        main_layout.addWidget(self.graph)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(46, 16, 46, 16)

        self.save_plot_button = Button("SAVE PLOT", self.stylesheet_red)
        self.save_plot_button.clicked.connect(self.save_graph)
        self.save_plot_button.installEventFilter(self)

        self.save_raw_button = Button("SAVE RAW DATA", self.stylesheet_grey)
        self.save_raw_button.clicked.connect(self.save_raw)
        self.save_raw_button.installEventFilter(self)

        buttons_layout.addWidget(self.save_plot_button)
        buttons_layout.addWidget(self.save_raw_button)
        main_layout.addLayout(buttons_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(main_widget)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            if obj == self.save_plot_button:
                self.save_plot_button.set_style("color: #F03C3C;background-color: white;border: 2px solid #F03C3C;")
                return True
            if obj == self.save_raw_button:
                self.save_raw_button.set_style("color: #EBEEF5;background-color: #6A6E77;")
                return True
        elif event.type() == QEvent.HoverLeave:
            if obj == self.save_plot_button:
                self.save_plot_button.set_style("color: white;background-color: #F03C3C;border: 2px solid transparent;")
                return True
            if obj == self.save_raw_button:
                self.save_raw_button.set_style("color: #6A6E77;background-color: #EBEEF5;")
                return True
        return super().eventFilter(obj, event)

    def save_graph(self):
        if os.path.isfile("../graphics/Example.png"):
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Image Files (*.png)', options=options)
            if file_name:
                shutil.copy("../graphics/Example.png", file_name)

    def save_raw(self):
        if self.data:
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV Files (*.csv)', options=options)
            if file_name:
                with open(file_name, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([f"Region {i+1}" for i in range(len(self.data[0]))])
                    writer.writerows(self.data)
