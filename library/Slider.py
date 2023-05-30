from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        self.setStyleSheet(
            '''
            QSlider::groove:horizontal {
                background: #6A6E77;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::sub-page:horizontal {
                background: #F03C3C;
                height: 8px;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #F03C3C;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            '''
        )
        self.setMinimum(1)
        self.setMaximum(1)
        self.setValue(1)
