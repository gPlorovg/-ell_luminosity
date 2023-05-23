from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup, QVBoxLayout,\
    QSlider, QLabel, QPushButton, QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGridLayout, QSizePolicy,\
    QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QIcon, QPixmap, QDragEnterEvent, QDragMoveEvent, QWheelEvent, QColor, QPen, QFont
from PyQt5.QtCore import QSize, QMargins, Qt, QPointF, QEvent, pyqtSlot, pyqtSignal


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


class Toolbar(QWidget):
    draw_mode = pyqtSignal(bool)
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

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon("../images/icons/light_theme/basic/save.svg"))
        self.save_button.setIconSize(icon_size)
        button_group.addButton(self.save_button)
        tools_layout.addWidget(self.save_button)
        # self.save_button.setObjectName("save_button")
        self.save_button.installEventFilter(self)

        self.colorize_button = QPushButton()
        self.colorize_button.setIcon(QIcon("../images/icons/light_theme/basic/colorize.svg"))
        self.colorize_button.setIconSize(icon_size)
        button_group.addButton(self.colorize_button)
        tools_layout.addWidget(self.colorize_button)
        # colorize_button.setObjectName("colorize_button")
        self.colorize_button.installEventFilter(self)

        self.shape_button = QPushButton()
        self.shape_button.setIcon(QIcon("../images/icons/light_theme/basic/shape.svg"))
        self.shape_button.setIconSize(icon_size)
        self.shape_button.setCheckable(True)
        button_group.addButton(self.shape_button)
        tools_layout.addWidget(self.shape_button)
        # shape_button.setObjectName("shape_button")
        self.shape_button.toggled.connect(self.turn_shape_mode)
        self.shape_button.installEventFilter(self)

        self.graph_button = QPushButton()
        self.graph_button.setIcon(QIcon("../images/icons/light_theme/basic/graph.svg"))
        self.graph_button.setIconSize(icon_size)
        button_group.addButton(self.graph_button)
        tools_layout.addWidget(self.graph_button)
        # graph_button.setObjectName("graph_button")
        self.graph_button.installEventFilter(self)

        self.setting_button = QPushButton()
        self.setting_button.setIcon(QIcon("../images/icons/light_theme/basic/settings.svg"))
        self.setting_button.setIconSize(icon_size)
        # setting_button.setSizePolicy(QSizePolicy.Fixed)
        # setting_button.setFixedSize(self.setting_button_size)
        button_group.addButton(self.setting_button)
        self.setting_button.setObjectName("setting_button")
        self.setting_button.installEventFilter(self)

        tool_bar_layout.addWidget(tools_widget)
        tool_bar_layout.addWidget(self.setting_button)
        tools_layout.setSpacing(10)
        self.setLayout(tool_bar_layout)
        self.setStyleSheet(stylesheet)
        self.setFixedSize(QSize(84, 360))

    def turn_shape_mode(self, mode):
        if mode:
            self.shape_button.setIcon(QIcon("../images/icons/light_theme/chosen/shape.svg"))
            self.draw_mode.emit(True)
        else:
            self.shape_button.setIcon(QIcon("../images/icons/light_theme/basic/shape.svg"))
            self.draw_mode.emit(False)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            if obj == self.save_button:
                self.save_button.setIcon(QIcon("../images/icons/light_theme/chosen/save.svg"))
                return True
            if obj == self.colorize_button:
                self.colorize_button.setIcon(QIcon("../images/icons/light_theme/chosen/colorize.svg"))
                return True
            if obj == self.shape_button and not self.shape_button.isChecked():
                self.shape_button.setIcon(QIcon("../images/icons/light_theme/chosen/shape.svg"))
                return True
            if obj == self.graph_button:
                self.graph_button.setIcon(QIcon("../images/icons/light_theme/chosen/graph.svg"))
                return True
            if obj == self.setting_button:
                self.setting_button.setIcon(QIcon("../images/icons/light_theme/chosen/settings.svg"))
                return True
        elif event.type() == QEvent.HoverLeave:
            if obj == self.save_button:
                self.save_button.setIcon(QIcon("../images/icons/light_theme/basic/save.svg"))
                return True
            if obj == self.colorize_button:
                self.colorize_button.setIcon(QIcon("../images/icons/light_theme/basic/colorize.svg"))
                return True
            if obj == self.shape_button and not self.shape_button.isChecked():
                self.shape_button.setIcon(QIcon("../images/icons/light_theme/basic/shape.svg"))
                return True
            if obj == self.graph_button:
                self.graph_button.setIcon(QIcon("../images/icons/light_theme/basic/graph.svg"))
                return True
            if obj == self.setting_button:
                self.setting_button.setIcon(QIcon("../images/icons/light_theme/basic/settings.svg"))
                return True
        return super().eventFilter(obj, event)


class Scene(QGraphicsScene):
    def __init__(self):
        super().__init__()
        self.pen = QPen(QColor("#F03C3C"), 4)
        self.pen.setStyle(Qt.CustomDashLine)
        self.pen.setDashPattern([3, 2])
        self.z_order = 1
        self.items_list = []
        self._start = None
        self._current_oval = None
        self.draw_mode = False

    def mousePressEvent(self, event):
        if self.draw_mode:
            if event.button() == Qt.LeftButton:
                self._start = event.scenePos()

    def mouseMoveEvent(self, event):
        if self.draw_mode:
            if event.buttons() & Qt.LeftButton:
                if self._current_oval is not None:
                    self.removeItem(self._current_oval)
                end = event.scenePos()
                x = min(self._start.x(), end.x())
                y = min(self._start.y(), end.y())
                r = max(abs(self._start.x() - end.x()), abs(self._start.y() - end.y()))
                self._current_oval = QGraphicsEllipseItem(x, y, r, r)
                self._current_oval.setPen(self.pen)
                if self._current_oval.zValue() < self.z_order:
                    self._current_oval.setZValue(self.z_order)
                self.addItem(self._current_oval)

    def mouseReleaseEvent(self, event):
        if self.draw_mode:
            if event.button() == Qt.LeftButton:
                if self._current_oval is not None:
                    self.removeItem(self._current_oval)
                end = event.scenePos()
                x = min(self._start.x(), end.x())
                y = min(self._start.y(), end.y())
                r = max(abs(self._start.x() - end.x()), abs(self._start.y() - end.y()))
                print(x, y, r)
                oval = QGraphicsEllipseItem(x, y, r, r)
                oval.setPen(self.pen)
                oval.setZValue(self.z_order)
                self.addItem(oval)

                center = oval.rect().center()
                text_item = QGraphicsTextItem(str(self.z_order))
                text_item.setFont(QFont("Inter", 10))
                text_item.setDefaultTextColor(QColor("#F03C3C"))
                text_item.setPos(center - QPointF(text_item.boundingRect().width() / 2,
                                                  text_item.boundingRect().height() / 2))
                self.addItem(text_item)

                self.items_list.append((oval, text_item, (round(center.x()), round(center.y()), round(r))))
                self.z_order += 1
                self._start = None
                self._current_oval = None
            elif event.button() == Qt.RightButton:
                self.removeItem(self.items_list[-1][0])
                self.removeItem(self.items_list[-1][1])
                self.items_list.pop(-1)
                self.z_order -= 1


class Viewer(QGraphicsView):
    def __init__(self, set_slider_max):
        super().__init__()
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.set_slider_max = set_slider_max
        self.image_paths = []
        self.setAcceptDrops(True)
        self.zoom = 1
        self.setFixedSize(QSize(500, 500))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = Scene()
        self.setScene(self.scene)

        self.image = QGraphicsPixmapItem(QPixmap("../data/1.jpg"))
        self.scene.addItem(self.image)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.zoom += 0.1
        else:
            self.zoom -= 0.1
        self.scale(self.zoom, self.zoom)
        self.zoom = 1

    def show_image(self, value):
        self.scene.removeItem(self.image)
        self.image = QGraphicsPixmapItem(QPixmap(self.image_paths[value]))
        self.scene.addItem(self.image)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent) -> None:
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            self.image_paths.clear()
            for url in event.mimeData().urls():
                self.image_paths.append(url.toLocalFile())
            self.image_paths.append(self.image_paths.pop(0))
            self.show_image(0)
            event.accept()
            self.set_slider_max(len(self.image_paths))
            self.scene.z_order = 1
        else:
            event.ignore()


class Slider(QSlider):
    def __init__(self):
        super().__init__(Qt.Horizontal)
        # self.setSizePolicy(QSizePolicy.Fixed)
        self.setStyleSheet(
            '''
                background-color: transparent;
            '''
        )
        self.setMinimum(1)
        self.setMaximum(1)
        self.setValue(1)


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
                font-size: 20px;
                line-height: 24px;
        '''
        self.setStyleSheet(stylesheet)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image_name = "Some image"
        self.current_frame = 0
        self.max_frame = 0
        self.image_paths = []
        self.images_names = dict()

        with open("style.qss", "r") as f:
            stylesheet = f.read()

        toolbar_layout = QVBoxLayout()
        # toolbar_layout.setStretch(1)
        toolbar_layout.setSpacing(10)
        self.toolbar = Toolbar(stylesheet)
        toolbar_layout.addWidget(self.toolbar)
        self.toolbar.draw_mode.connect(self.turn_draw_mode)

        workspace_layout = QGridLayout()
        workspace_layout.setSpacing(2)

        self.image_label = MyLabel("NAME")
        self.image_label.set_text(self.image_name)
        workspace_layout.addWidget(self.image_label, 0, 0)

        self.picture_viewer = Viewer(self.set_slider_max)
        workspace_layout.addWidget(self.picture_viewer, 1, 0, 2, 2)

        self.slider = Slider()
        self.slider.valueChanged.connect(self.change_image)
        workspace_layout.addWidget(self.slider, 3, 0)

        self.frame_label = MyLabel("FRAME")
        self.frame_label.set_text("1", " / ", "?")
        workspace_layout.addWidget(self.frame_label, 3, 1)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(QMargins(20, 20, 20, 20))
        main_layout.setSpacing(20)
        main_layout.addLayout(toolbar_layout)
        main_layout.addLayout(workspace_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(main_widget)

    def change_image(self, value):
        self.frame_label.set_text(str(value), " / ", str(self.slider.maximum()))

        if value not in self.images_names:
            self.images_names[value] = self.picture_viewer.image_paths[value - 1]\
                [self.picture_viewer.image_paths[value-1].rfind("/") + 1:]
            self.image_label.set_text(self.images_names[value])
        else:
            self.image_label.set_text(self.images_names[value])

        self.picture_viewer.show_image(value - 1)

    def set_slider_max(self, val):
        self.slider.setMaximum(val)

    @pyqtSlot(bool)
    def turn_draw_mode(self, checked):
        if checked:
            self.picture_viewer.scene.draw_mode = True
            self.picture_viewer.setDragMode(QGraphicsView.NoDrag)
        else:
            self.picture_viewer.scene.draw_mode = False
            self.picture_viewer.setDragMode(QGraphicsView.ScrollHandDrag)


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

        main_layout = QVBoxLayout()
        image_label = MyLabel("NAME", image_name)
        main_layout.addWidget(image_label)

        graph = Graph()
        main_layout.addWidget(graph)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setContentsMargins(46, 16, 46, 16)
        save_plot_button = Button("SAVE PLOT", stylesheet_red)
        save_raw_button = Button("SAVE RAW DATA", stylesheet_grey)
        buttons_layout.addWidget(save_plot_button)
        buttons_layout.addWidget(save_raw_button)
        main_layout.addLayout(buttons_layout)

        main_widget = QWidget(self)
        main_widget.setLayout(main_layout)
        main_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(main_widget)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()