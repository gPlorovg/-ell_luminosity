from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, \
    QHBoxLayout, QWidget, QGraphicsView, QGridLayout, QFileDialog, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QMargins, pyqtSlot, pyqtSignal
import csv
import os
import json
from library import proceccing
from library.Observe import Observable
from library.Toolbar import Toolbar
from library.Label import MyLabel
from library.PictureViewer import Viewer
from library.Slider import Slider
from library.GraghWindow import GraphWindow
from library.SettingsWindow import SettingsWindow


class SaveMenu(QMenu):
    leave = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.save_roi = QAction("Save regions of interest", self)
        self.open_roi = QAction("Open regions of interest", self)
        self.save_current_frame = QAction("Save current frame", self)
        self.save_graph = QAction("Save plot", self)
        self.save_raw_data = QAction("Save raw data", self)

        self.addAction(self.save_roi)
        self.addAction(self.open_roi)
        self.addAction(self.save_current_frame)
        self.addAction(self.save_graph)
        self.addAction(self.save_raw_data)

    def leaveEvent(self, event) -> None:
        self.leave.emit()


class MainWindow(QMainWindow, Observable):
    def __init__(self):
        super().__init__()
        self.curr_image_name = "~image name~"
        self.image_names = dict()
        self.current_frame = 0
        self.roi = list()
        self.frame_data = list()

        with open("settings/style.qss", "r") as f:
            self.stylesheet = f.read()

        self.init_ui()

    def init_ui(self):
        self.attach(self)
        self.graph_window = GraphWindow()
        self.attach(self.graph_window)

        self.settings_window = SettingsWindow()
        self.attach(self.settings_window)
        self.settings_window.dark_mode.connect(self.notify)

        toolbar_layout = QVBoxLayout()
        toolbar_layout.setSpacing(10)
        self.toolbar = Toolbar(self.stylesheet)
        self.attach(self.toolbar)
        toolbar_layout.addWidget(self.toolbar)
        self.toolbar.draw_mode.connect(self.turn_draw_mode)
        self.toolbar.colorize_button.clicked.connect(self.colorize_cur_frame)
        self.toolbar.graph_button.clicked.connect(self.calculate)
        self.toolbar.setting_button.clicked.connect(self.settings_window.show)

        self.save_menu = SaveMenu()
        self.attach(self.save_menu)
        self.save_menu.leave.connect(
            lambda: self.toolbar.save_button.setIcon(QIcon("../images/icons/light_theme/basic/save.svg")))

        self.save_menu.save_graph.triggered.connect(self.graph_window.save_graph)
        self.save_menu.save_raw_data.triggered.connect(self.graph_window.save_raw)
        self.save_menu.save_roi.triggered.connect(self.save_roi)
        self.save_menu.open_roi.triggered.connect(self.open_roi)
        self.save_menu.save_current_frame.triggered.connect(self.save_cur_frame)
        self.toolbar.save_button.setMenu(self.save_menu)

        workspace_layout = QGridLayout()
        workspace_layout.setSpacing(2)

        self.image_label = MyLabel("NAME")
        self.attach(self.image_label)
        self.image_label.set_text(self.curr_image_name)
        workspace_layout.addWidget(self.image_label, 0, 0)

        self.picture_viewer = Viewer()
        self.attach(self.picture_viewer)
        self.picture_viewer.add_pictures.connect(self.handle_add_pics)
        workspace_layout.addWidget(self.picture_viewer, 1, 0, 2, 2)

        self.slider = Slider()
        self.attach(self.slider)
        self.slider.valueChanged.connect(self.change_image)
        workspace_layout.addWidget(self.slider, 3, 0)

        self.frame_label = MyLabel("FRAME")
        self.attach(self.frame_label)
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
        # change value of frame counter
        self.frame_label.set_text(str(value), " / ", str(self.slider.maximum()))
        # add "clean" image name to cache
        if value not in self.image_names:
            last_picture = self.picture_viewer.image_paths[value - 1]
            self.image_names[value] = last_picture[last_picture.rfind("/") + 1:]
            # change image name
            self.image_label.set_text(self.image_names[value])
        else:
            self.image_label.set_text(self.image_names[value])
        # show image in viewer
        self.picture_viewer.show_image(value - 1)

    def set_slider_max(self, val):
        self.slider.setMaximum(val)
        # setup frame counter values
        self.frame_label.set_text(str(self.slider.minimum()), " / ", str(self.slider.maximum()))

    @pyqtSlot(int)
    def handle_add_pics(self, quantity_of_pics):
        self.set_slider_max(quantity_of_pics)
        # init first image name
        self.image_names[1] = self.picture_viewer.image_paths[0][self.picture_viewer.image_paths[0].rfind("/") + 1:]
        self.image_label.set_text(self.image_names[1])
        # unfreeze toolbar interface
        self.toolbar.tools_widget.setEnabled(True)

    @pyqtSlot(bool)
    def turn_draw_mode(self, checked):
        if checked:
            self.picture_viewer.scene.draw_mode = True
            self.picture_viewer.setDragMode(QGraphicsView.NoDrag)
        else:
            self.picture_viewer.scene.draw_mode = False
            self.picture_viewer.setDragMode(QGraphicsView.ScrollHandDrag)

    def calculate(self):
        # if at least one circle(roi) in scene exists
        if self.picture_viewer.scene.items_list:
            # calculate all roi in scene
            self.roi = [proceccing.ROI(*el[2]) for el in self.picture_viewer.scene.items_list]
            self.frame_data = []
            # calculate measure fluorescence in each roi for each image
            for url in self.picture_viewer.image_paths:
                self.frame_data.append([roi.measure(proceccing.open_image(url)) for roi in self.roi])

            self.graph_window.graph.setPixmap(QPixmap(proceccing.make_graph(self.frame_data, "Example")))
            self.graph_window.data = self.frame_data
            # set first image name as graph name label
            self.graph_window.image_label.set_text(self.image_names[1])
            self.graph_window.show()

        # Example of frame_data
        #     roi1 roi2   roi3   roi4
        # fr1[0.0, 138.0, 130.0, 111.0]
        # fr2[0.0, 17.0, 16.0, 14.0]
        # fr3[0.0, 24.0, 21.0, 15.0]
        # fr4[0.0, 74.0, 70.0, 59.0]

    def save_roi(self):
        if self.picture_viewer.scene.items_list:
            # calculate all roi in scene
            self.roi = [proceccing.ROI(*el[2]) for el in self.picture_viewer.scene.items_list]
            # show save file dialog window
            options = QFileDialog.Options()
            file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'CSV Files (*.csv)', options=options)
            # save roi as csv file
            if file_name:
                with open(file_name, "w", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow(["", "X", "Y", "R"])
                    writer.writerows([[f"Region {i+1}", *roi.get_info()] for i, roi in enumerate(self.roi)])

    def open_roi(self):
        # show open file dialog window
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open File")

        if file_path:
            with open(file_path, 'r') as file:
                reader = csv.reader(file)
                _ = next(reader)  # Read the header row
                data = []
                # getting all data about roi
                for row in reader:
                    data.append(list(map(lambda el: int(el), row[1:])))
            # add roi to scene
            for roi in data:
                self.picture_viewer.scene.add_oval(*roi)

    def save_cur_frame(self):
        # show save file dialog window
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Image Files (*.png)', options=options)

        if file_name:
            # save current image
            self.picture_viewer.image.pixmap().save(file_name)

    # colorized current picture without influence on data for calculating fluorescence
    def colorize_cur_frame(self):
        colorized_pixmap = proceccing.colorize(self.picture_viewer.image.pixmap(),
                                               self.settings_window.settings["cmap"])
        self.picture_viewer.show_image(pixmap=colorized_pixmap)

    # change theme mode
    # def update_(self, dark_mode):
    #     self.setStyleSheet()

    # executes when program closing
    def closeEvent(self, e) -> None:
        # remove Example file - temporary file that contains last calculated graph
        if os.path.isfile("../graphics/Example.png"):
            os.remove("../graphics/Example.png")
        # saving settings
        with open("settings/config.json", "w") as f:
            json.dump(self.settings_window.settings, f)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
