from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy
from library.Observe import Observer


class MyLabel(QWidget, Observer):
    def __init__(self, title):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(6)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("title_label")
        self.layout.addWidget(self.title_label)

        self.data_label = QLabel()
        self.data_label.setObjectName("data_label")
        self.layout.addWidget(self.data_label)
        self.setLayout(self.layout)

    def set_text(self, *args):
        s = "".join([str(i) for i in args])
        self.data_label.setText(s)
