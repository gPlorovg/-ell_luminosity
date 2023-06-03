from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize, Qt, QEvent

import csv
import shutil
import os

from library.Label import MyLabel
from library.Observe import Observer


class Graph(QLabel):
    def __init__(self):
        super().__init__()
        self.setPixmap(QPixmap("../images/cat.jpg"))
        self.setFixedSize(QSize(500, 500))
        self.setAlignment(Qt.AlignCenter)


class GraphWindow(QMainWindow, Observer):
    def __init__(self):
        super().__init__()
        self.data = list()
        self.buttons_stylesheets = dict()
        self.mode_path = "dark" if self.dark_mode else "light"
        self.init_buttons_stylesheets()

        main_layout = QVBoxLayout()
        self.image_label = MyLabel("NAME")
        self.image_label.update_(self.dark_mode)
        self.image_label.set_text("Some image")
        main_layout.addWidget(self.image_label)

        self.graph = Graph()
        main_layout.addWidget(self.graph)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(46, 16, 46, 16)

        self.save_plot_button = QPushButton("SAVE PLOT")
        self.save_plot_button.setObjectName("save_plot_button")
        self.save_plot_button.clicked.connect(self.save_graph)
        self.save_plot_button.installEventFilter(self)

        self.save_raw_button = QPushButton("SAVE RAW DATA")
        self.save_raw_button.setObjectName("save_raw_button")
        self.save_raw_button.clicked.connect(self.save_raw)
        self.save_raw_button.installEventFilter(self)

        buttons_layout.addWidget(self.save_plot_button)
        buttons_layout.addWidget(self.save_raw_button)
        main_layout.addLayout(buttons_layout)

        self.setObjectName("graph_window")
        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def init_buttons_stylesheets(self):
        self.buttons_stylesheets["plot_basic_light"] = \
            "color: white;background-color: #F03C3C;border: 2px solid transparent;"
        self.buttons_stylesheets["plot_basic_dark"] = \
            "color: #1E1E1E;background-color: #A2D01E;border: 2px solid transparent;"
        self.buttons_stylesheets["plot_chosen_light"] = \
            "color: #F03C3C;background-color: white;border: 2px solid #F03C3C;"
        self.buttons_stylesheets["plot_chosen_dark"] = \
            "color: #A2D01E;background-color: #1E1E1E;border: 2px solid #A2D01E;"

        self.buttons_stylesheets["raw_basic_light"] = \
            "color: #6A6E77;background-color: #EBEEF5;"
        self.buttons_stylesheets["raw_basic_dark"] = \
            "color: #F0F0F0;background-color: #282828;"
        self.buttons_stylesheets["raw_chosen_light"] = \
            "color: #EBEEF5;background-color: #6A6E77;"
        self.buttons_stylesheets["raw_chosen_dark"] = \
            "color: #282828;background-color: #F0F0F0;"

    def update_buttons(self):
        self.save_plot_button.setStyleSheet(self.buttons_stylesheets[f"plot_basic_{self.mode_path}"])
        self.save_raw_button.setStyleSheet(self.buttons_stylesheets[f"raw_basic_{self.mode_path}"])

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            if obj == self.save_plot_button:
                self.save_plot_button.setStyleSheet(self.buttons_stylesheets[f"plot_chosen_{self.mode_path}"])
                return True
            if obj == self.save_raw_button:
                self.save_raw_button.setStyleSheet(self.buttons_stylesheets[f"raw_chosen_{self.mode_path}"])
                return True
        elif event.type() == QEvent.HoverLeave:
            if obj == self.save_plot_button:
                self.save_plot_button.setStyleSheet(self.buttons_stylesheets[f"plot_basic_{self.mode_path}"])
                return True
            if obj == self.save_raw_button:
                self.save_raw_button.setStyleSheet(self.buttons_stylesheets[f"raw_basic_{self.mode_path}"])
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
