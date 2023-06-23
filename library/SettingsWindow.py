from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QHBoxLayout, QWidget, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QEvent, pyqtSignal

import json
from library.Observe import Observer


class ThemeModeButton(QPushButton):
    def __init__(self, dark_mode):
        super().__init__()
        self.setCheckable(True)
        self.setChecked(dark_mode)
        self.setFixedSize(QSize(210, 45))
        self.setIconSize(QSize(210, 45))

        if dark_mode:
            self.setIcon(QIcon("images/theme_mode_button_icons/dark_mode.png"))
        else:
            self.setIcon(QIcon("images/theme_mode_button_icons/light_mode.png"))


class CmapList(QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(468, 40)
        self.setIconSize(QSize(380, 40))

        self.addItem(QIcon("images/cmaps/magma.png"), "magma")
        self.addItem(QIcon("images/cmaps/viridis.png"), "viridis")
        self.addItem(QIcon("images/cmaps/plasma.png"), "plasma")
        self.addItem(QIcon("images/cmaps/inferno.png"), "inferno")
        self.addItem(QIcon("images/cmaps/cividis.png"), "cividis")


class SettingsWindow(QMainWindow, Observer):
    is_dark_mode = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setFixedSize(QSize(500, 250))
        self.main_layout = QVBoxLayout()
        self.layout = QHBoxLayout()
        self.settings = dict()
        self.tmp_settings = dict()
        self.buttons_stylesheets = dict()
        self.init_buttons_stylesheets()

        with open("scripts/settings/config.json") as f:
            self.settings = json.load(f)

        self.mode_path = "dark" if self.settings["dark_mode"] else "light"
        self.tmp_settings = self.settings.copy()

        self.theme_mode_button = ThemeModeButton(self.settings["dark_mode"])
        self.theme_mode_button_layout = QHBoxLayout()
        self.theme_mode_button_layout.addWidget(self.theme_mode_button)
        self.theme_mode_button_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(self.theme_mode_button_layout)
        self.theme_mode_button.clicked.connect(self.change_mode)
        self.theme_mode_button.setObjectName("theme_mode_button")

        self.cmap = CmapList()
        self.cmap.setCurrentText(self.settings["cmap"])
        self.cmap.setObjectName("cmap_list")
        self.main_layout.addWidget(self.cmap)
        self.cmap.currentTextChanged.connect(self.change_cmap)

        self.apply_b = QPushButton("Apply")
        self.apply_b.setObjectName("apply_b")
        self.layout.addWidget(self.apply_b)
        self.apply_b.installEventFilter(self)
        self.apply_b.clicked.connect(self.apply)

        self.cancel_b = QPushButton("Cancel")
        self.cancel_b.setObjectName("cancel_b")
        self.layout.addWidget(self.cancel_b)
        self.cancel_b.installEventFilter(self)
        self.cancel_b.clicked.connect(self.close_)

        self.main_layout.setAlignment(Qt.AlignCenter)
        self.layout.setAlignment(Qt.AlignCenter)
        self.main_layout.setSpacing(40)

        self.main_layout.addLayout(self.layout)

        self.setObjectName("settings_window")

        self.widget = QWidget()
        self.widget.setLayout(self.main_layout)
        self.setCentralWidget(self.widget)

    def change_mode(self, dark_mode):
        if dark_mode:
            self.theme_mode_button.setIcon(QIcon("images/theme_mode_button_icons/dark_mode.png"))
        else:
            self.theme_mode_button.setIcon(QIcon("images/theme_mode_button_icons/light_mode.png"))
        self.tmp_settings["dark_mode"] = dark_mode
        self.is_dark_mode.emit(dark_mode)

    def change_cmap(self, cmap):
        self.cmap.setCurrentText(cmap)
        self.tmp_settings["cmap"] = cmap

    def close_(self):
        self.change_mode(self.settings["dark_mode"])
        self.change_cmap(self.settings["cmap"])
        self.close()

    def apply(self):
        self.settings = self.tmp_settings.copy()
        self.close()

    def init_buttons_stylesheets(self):
        self.buttons_stylesheets["apply_basic_light"] = \
            "color: white;background-color: #F03C3C;border: 2px solid transparent;"
        self.buttons_stylesheets["apply_basic_dark"] = \
            "color: #1E1E1E;background-color: #A2D01E;border: 2px solid transparent;"
        self.buttons_stylesheets["apply_chosen_light"] = \
            "color: #F03C3C;background-color: white;border: 2px solid #F03C3C;"
        self.buttons_stylesheets["apply_chosen_dark"] = \
            "color: #A2D01E;background-color: #1E1E1E;border: 2px solid #A2D01E;"

        self.buttons_stylesheets["cancel_basic_light"] = \
            "color: #6A6E77;background-color: #EBEEF5;"
        self.buttons_stylesheets["cancel_basic_dark"] = \
            "color: #F0F0F0;background-color: #282828;"
        self.buttons_stylesheets["cancel_chosen_light"] = \
            "color: #EBEEF5;background-color: #6A6E77;"
        self.buttons_stylesheets["cancel_chosen_dark"] = \
            "color: #282828;background-color: #F0F0F0;"

    def update_buttons(self):
        self.apply_b.setStyleSheet(self.buttons_stylesheets[f"apply_basic_{self.mode_path}"])
        self.cancel_b.setStyleSheet(self.buttons_stylesheets[f"cancel_basic_{self.mode_path}"])

    # handel hovering apply and close buttons
    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            if obj == self.apply_b:
                self.apply_b.setStyleSheet(self.buttons_stylesheets[f"apply_chosen_{self.mode_path}"])
                return True
            if obj == self.cancel_b:
                self.cancel_b.setStyleSheet(self.buttons_stylesheets[f"cancel_chosen_{self.mode_path}"])
                return True
        elif event.type() == QEvent.HoverLeave:
            if obj == self.apply_b:
                self.apply_b.setStyleSheet(self.buttons_stylesheets[f"apply_basic_{self.mode_path}"])
                return True
            if obj == self.cancel_b:
                self.cancel_b.setStyleSheet(self.buttons_stylesheets[f"cancel_basic_{self.mode_path}"])
                return True
        return super().eventFilter(obj, event)
