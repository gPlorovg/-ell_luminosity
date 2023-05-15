from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QVBoxLayout,\
    QSlider, QLabel, QPushButton, QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGridLayout, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import Qt, QSize, QEvent, QMargins


class MyLabel(QWidget):
    def __init__(self, title, *args):
        super().__init__()
        layout = QHBoxLayout()
        layout.setSpacing(6)
        title_label = QLabel(title)
        # title_label.setSizePolicy(QSizePolicy.Fixed)
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
        layout.addWidget(title_label)

        s = "".join([str(i) for i in args])
        data_label = QLabel(s)
        # data_label.setSizePolicy(QSizePolicy.Fixed)
        data_label.setStyleSheet(
            '''
                font-family: 'Inter';
                font-style: normal;
                font-weight: 400;
                font-size: 16px;
                line-height: 24px;
                color: #6A6E77;
            '''
        )
        layout.addWidget(data_label)
        self.setLayout(layout)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


class Toolbar(QWidget):
    def __init__(self, stylesheet):
        super().__init__()
        icon_size = QSize(32, 32)
        tool_bar_layout = QVBoxLayout()

        tools_widget = QWidget()
        tools_layout = QVBoxLayout()
        tools_widget.setLayout(tools_layout)
        tools_widget.setObjectName("tools_widget")
        # tools_widget.setSizePolicy(QSizePolicy.Fixed)

        button_group = QButtonGroup()
        # button_group.setExclusive(True)

        save_button = QPushButton()
        save_button.setIcon(QIcon("../images/icons/light_theme/basic/save.svg"))
        save_button.setIconSize(icon_size)
        button_group.addButton(save_button)
        tools_layout.addWidget(save_button)
        save_button.setObjectName("save_button")

        colorize_button = QPushButton()
        colorize_button.setIcon(QIcon("../images/icons/light_theme/basic/colorize.svg"))
        colorize_button.setIconSize(icon_size)
        button_group.addButton(colorize_button)
        tools_layout.addWidget(colorize_button)
        # colorize_button.setObjectName("colorize_button")

        shape_button = QPushButton()
        shape_button.setIcon(QIcon("../images/icons/light_theme/basic/shape.svg"))
        shape_button.setIconSize(icon_size)
        save_button.setCheckable(True)
        button_group.addButton(shape_button)
        tools_layout.addWidget(shape_button)
        # shape_button.setObjectName("shape_button")

        graph_button = QPushButton()
        graph_button.setIcon(QIcon("../images/icons/light_theme/basic/graph.svg"))
        graph_button.setIconSize(icon_size)
        button_group.addButton(graph_button)
        tools_layout.addWidget(graph_button)
        # graph_button.setObjectName("graph_button")

        setting_button = QPushButton()
        setting_button.setIcon(QIcon("../images/icons/light_theme/basic/settings.svg"))
        setting_button.setIconSize(icon_size)
        # setting_button.setSizePolicy(QSizePolicy.Fixed)
        # setting_button.setFixedSize(self.setting_button_size)
        button_group.addButton(setting_button)
        setting_button.setObjectName("setting_button")

        tool_bar_layout.addWidget(tools_widget)
        tool_bar_layout.addWidget(setting_button)
        tools_layout.setSpacing(10)
        self.setLayout(tool_bar_layout)
        self.setStyleSheet(stylesheet)
        self.setFixedSize(QSize(84, 360))


class Viewer(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("../data/1.jpg")
        self.setPixmap(pixmap)
        self.setFixedSize(QSize(500, 500))
        self.setAlignment(Qt.AlignCenter)


class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        # self.setSizePolicy(QSizePolicy.Fixed)
        self.setStyleSheet(
            '''
                background-color: transparent;
            '''
        )


class Graph(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap("../data/1.jpg")
        self.setPixmap(pixmap)
        self.setFixedSize(QSize(500, 500))
        self.setAlignment(Qt.AlignCenter)


class Button(QPushButton):
    def __init__(self, text, stylesheet):
        super().__init__(text)
        stylesheet += '''
                border-radius: 10px;
                padding: 10px;
                min-height: 32px;
                max-width: 250px;
                
                font-family: 'Inter';
                font-style: normal;
                font-weight: 700;
                font-size: 16px;
                line-height: 24px;
        '''
        self.setStyleSheet(stylesheet)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        image_name = "Some image"
        current_frame = 8
        max_frame = 12

        with open("style.qss", "r") as f:
            stylesheet = f.read()

        toolbar_layout = QVBoxLayout()
        # toolbar_layout.setStretch(1)
        toolbar_layout.setSpacing(10)
        toolbar = Toolbar(stylesheet)
        toolbar_layout.addWidget(toolbar)

        workspace_layout = QGridLayout()
        workspace_layout.setSpacing(2)
        image_label = MyLabel("NAME", image_name)
        workspace_layout.addWidget(image_label, 0, 0)
        picture_viewer = Viewer()
        workspace_layout.addWidget(picture_viewer, 1, 0, 2, 2)
        slider = Slider()
        workspace_layout.addWidget(slider, 3, 0)
        frame_label = MyLabel("FRAME", current_frame, " / ", max_frame)
        workspace_layout.addWidget(frame_label, 3, 1)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(QMargins(20, 20, 20, 20))
        main_layout.setSpacing(20)
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(workspace_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(main_widget)


class GraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        image_name = "Some image"
        stylesheet_red = '''
                color: white;
                background-color: #F03C3C;
        '''
        stylesheet_grey = '''
                color: #6A6E77;
                background-color: #EBEEF5;
        '''

        main_layout = QGridLayout()
        main_layout.setSpacing(16)
        image_label = MyLabel("NAME", image_name)
        main_layout.addWidget(image_label, 0, 0)

        graph = Graph()
        main_layout.addWidget(graph, 1, 0, 2, 2)

        save_plot_button = Button("SAVE PLOT", stylesheet_red)
        save_raw_button = Button("SAVE RAW DATA", stylesheet_grey)
        main_layout.addWidget(save_plot_button, 3, 0)
        main_layout.addWidget(save_raw_button, 3, 1)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white; padding: 16px;")
        self.setCentralWidget(main_widget)


if __name__ == '__main__':
    app = QApplication([])
    window = GraphWindow()
    window.show()
    app.exec_()