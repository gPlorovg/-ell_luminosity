from PyQt5.QtWidgets import QProgressBar
from library.Observe import Observer


class ProgressBarWindow(QProgressBar, Observer):
    def __init__(self):
        super().__init__()
        self.setMinimum(0)
        self.setMaximum(30)
        self.setTextVisible(False)

