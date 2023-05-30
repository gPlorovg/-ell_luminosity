from PyQt5.QtCore import QSize, QPoint
from PyQt5.QtGui import QImage, QIcon, QPixmap, QPainter
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget
from PIL import Image, ImageQt


class ToolBarButton(QPushButton):
    def __init__(self, icon: QIcon):
        super().__init__()
        self.setFixedSize(QSize(40, 40))
        self.setIcon(icon)


class ToolBar(QWidget):
    def colorize(self):
        self.buttons[0].setIcon(QIcon("c_colorize.svg"))

    def __init__(self):
        super().__init__()
        self.setFixedSize(40, 120)
        layout = QVBoxLayout()
        # main_layout.setSpacing(0)

        self.buttons = {
            0: ToolBarButton(QIcon("colorize.svg"))
        }

        layout.setContentsMargins(0, 0, 0, 0)
        print(layout.getContentsMargins())
        self.buttons[0].clicked.connect(self.colorize)
        layout.addWidget(self.buttons[0])
        # main_layout.addWidget(ToolBarButton(QIcon("save.svg")))
        # main_layout.addWidget(ToolBarButton(QIcon("plot.svg")))

        self.setLayout(layout)




class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(QSize(500, 500))
        self.setWindowTitle("Привет, Артём")
        self.central_widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(ToolBar())
        self.img = QLabel()
        self.img.setPixmap(QPixmap("4cividis.png"))
        layout.addWidget(self.img)
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self.drawer(500, 500)
        self.drawer(30, 100)


    def drawer(self, x, y):
        painter = QPainter(self.img.pixmap())
        # draw from center in point x, y
        # painter.drawEllipse(QPoint(x,y), 100, 100)

        # draw like a rectangle
        painter.drawEllipse(QPoint(x, y), 100, 100)
        painter.end()



app = QApplication([])

window = MainWindow()
window.show()

app.exec()
