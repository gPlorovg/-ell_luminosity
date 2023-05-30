from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

from library.Observe import Observer


class Slider(QSlider, Observer):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setMinimum(1)
        self.setMaximum(1)
        self.setValue(1)
