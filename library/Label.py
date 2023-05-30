from PyQt5.QtWidgets import QLabel, QHBoxLayout, QWidget, QSizePolicy


class MyLabel(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(6)
        title_label = QLabel(title)
        title_label.setStyleSheet(
            '''
                font-family: 'Inter';
                font-style: normal;
                font-weight: 700;
                font-size: 16px;
                line-height: 24px;
                color: #6A6E77;
            '''
        )
        self.layout.addWidget(title_label)
        self.data_label = QLabel()
        self.data_label.setStyleSheet(
            '''
                font-family: 'Inter';
                font-style: normal;
                font-weight: 400;
                font-size: 18px;
                line-height: 24px;
                color: #6A6E77;
            '''
        )
        self.layout.addWidget(self.data_label)
        self.setLayout(self.layout)

    def set_text(self, *args):
        s = "".join([str(i) for i in args])
        self.data_label.setText(s)
