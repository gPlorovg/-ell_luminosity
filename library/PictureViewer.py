from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QPixmap, QDragEnterEvent, QDragMoveEvent, QWheelEvent, QColor, QPen, QFont
from PyQt5.QtCore import QSize, Qt, QPointF, pyqtSignal
from library.Observe import Observer


class Scene(QGraphicsScene):
    def __init__(self, dark_mode):
        super().__init__()
        self.dark_mode = dark_mode
        self.color = "#A2D01E" if self.dark_mode else "#F03C3C"
        self.pen_light = QPen(QColor("#F03C3C"), 4)
        self.pen_light.setStyle(Qt.CustomDashLine)
        self.pen_light.setDashPattern([3, 2])

        self.pen_dark = QPen(QColor("#A2D01E"), 4)
        self.pen_dark.setStyle(Qt.CustomDashLine)
        self.pen_dark.setDashPattern([3, 2])

        self.pen = self.pen_dark if self.dark_mode else self.pen_light

        self.z_order = 1
        self.items_list = list()
        self._start = None
        self._current_oval = None
        self.draw_mode = False

    def __prepare_for_oval(self, event):
        if self._current_oval is not None:
            self.removeItem(self._current_oval)
        end = event.scenePos()
        x = min(self._start.x(), end.x())
        y = min(self._start.y(), end.y())
        r = max(abs(self._start.x() - end.x()), abs(self._start.y() - end.y()))

        return x, y, r

    def mousePressEvent(self, event):
        if self.draw_mode:
            if event.button() == Qt.LeftButton:
                self._start = event.scenePos()

    def mouseMoveEvent(self, event):
        if self.draw_mode:
            if event.buttons() & Qt.LeftButton:
                x, y, r = self.__prepare_for_oval(event)
                self._current_oval = QGraphicsEllipseItem(x, y, r, r)
                self._current_oval.setPen(self.pen)
                if self._current_oval.zValue() < self.z_order:
                    self._current_oval.setZValue(self.z_order)
                self.addItem(self._current_oval)

    def mouseReleaseEvent(self, event):
        if self.draw_mode:
            if event.button() == Qt.LeftButton:
                x, y, r = self.__prepare_for_oval(event)
                self.add_oval(x, y, r)

                self._start = None
                self._current_oval = None
            elif event.button() == Qt.RightButton:
                if self.items_list:
                    self.removeItem(self.items_list[-1][0])
                    self.removeItem(self.items_list[-1][1])
                    self.items_list.pop(-1)
                    self.z_order -= 1

    def add_oval(self, x, y, r):
        oval = QGraphicsEllipseItem(x, y, r, r)
        oval.setPen(self.pen)
        oval.setZValue(self.z_order)
        self.addItem(oval)

        center = oval.rect().center()
        text_item = QGraphicsTextItem(str(self.z_order))
        text_item.setFont(QFont("Inter", 10))
        text_item.setDefaultTextColor(QColor(self.color))
        text_item.setPos(center - QPointF(text_item.boundingRect().width() / 2,
                                          text_item.boundingRect().height() / 2))
        text_item.setZValue(self.z_order)
        self.addItem(text_item)

        self.items_list.append((oval, text_item, (round(center.x()), round(center.y()), round(r))))
        self.z_order += 1

    def repaint(self):
        for i in self.items_list:
            i[0].setPen(self.pen)
            i[1].setDefaultTextColor(QColor(self.color))


class Viewer(QGraphicsView, Observer):
    add_pictures = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        self.image_paths = []
        self.setAcceptDrops(True)
        self.zoom = 1
        self.max_resolution = 2_000_000
        self.setFixedSize(QSize(500, 500))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scene = Scene(self.dark_mode)
        self.scene.setObjectName("scene")
        self.setScene(self.scene)

        self.image = QGraphicsPixmapItem(QPixmap("images/default_image.png"))
        self.image_view_size = self.image.pixmap().size()
        self.scene.addItem(self.image)

    # boundaries correct works with the same size pictures
    def wheelEvent(self, event: QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            if max(self.image_view_size.width(), self.image_view_size.height()) < self.max_resolution:
                self.zoom += 0.1

        else:
            if not(self.image_view_size.width() < self.geometry().size().width()
                    and self.image_view_size.height() < self.geometry().size().height()):
                self.zoom -= 0.1
        self.scale(self.zoom, self.zoom)
        self.image_view_size *= self.zoom
        self.zoom = 1

    def show_image(self, value=0, pixmap=None):
        if pixmap is None:
            self.scene.removeItem(self.image)
            self.image = QGraphicsPixmapItem(QPixmap(self.image_paths[value]))
            self.scene.addItem(self.image)
        else:
            self.scene.removeItem(self.image)
            self.image = QGraphicsPixmapItem(pixmap)
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
            self.image_view_size = QPixmap(self.image_paths[0]).size()
            self.show_image(0)
            self.scene.z_order = 1
            self.add_pictures.emit(len(self.image_paths))
            event.accept()
        else:
            event.ignore()
