from PyQt5.QtWidgets import QButtonGroup, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QEvent, pyqtSignal


class Toolbar(QWidget):
    draw_mode = pyqtSignal(bool)

    def __init__(self, stylesheet):
        super().__init__()
        icon_size = QSize(32, 32)
        tool_bar_layout = QVBoxLayout()

        self.tools_widget = QWidget()
        tools_layout = QVBoxLayout()
        self.tools_widget.setLayout(tools_layout)
        self.tools_widget.setObjectName("tools_widget")
        self.tools_widget.setEnabled(False)

        button_group = QButtonGroup()

        self.save_button = QPushButton()
        self.save_button.setIcon(QIcon("../images/icons/light_theme/basic/save.svg"))
        self.save_button.setIconSize(icon_size)
        button_group.addButton(self.save_button)
        tools_layout.addWidget(self.save_button)
        self.save_button.installEventFilter(self)

        self.colorize_button = QPushButton()
        self.colorize_button.setIcon(QIcon("../images/icons/light_theme/basic/colorize.svg"))
        self.colorize_button.setIconSize(icon_size)
        button_group.addButton(self.colorize_button)
        tools_layout.addWidget(self.colorize_button)
        self.colorize_button.installEventFilter(self)

        self.shape_button = QPushButton()
        self.shape_button.setIcon(QIcon("../images/icons/light_theme/basic/shape.svg"))
        self.shape_button.setIconSize(icon_size)
        self.shape_button.setCheckable(True)
        button_group.addButton(self.shape_button)
        tools_layout.addWidget(self.shape_button)
        self.shape_button.toggled.connect(self.turn_shape_mode)
        self.shape_button.installEventFilter(self)

        self.graph_button = QPushButton()
        self.graph_button.setIcon(QIcon("../images/icons/light_theme/basic/graph.svg"))
        self.graph_button.setIconSize(icon_size)
        button_group.addButton(self.graph_button)
        tools_layout.addWidget(self.graph_button)
        self.graph_button.installEventFilter(self)

        self.setting_button = QPushButton()
        self.setting_button.setIcon(QIcon("../images/icons/light_theme/basic/settings.svg"))
        self.setting_button.setIconSize(icon_size)
        button_group.addButton(self.setting_button)
        self.setting_button.setObjectName("setting_button")
        self.setting_button.installEventFilter(self)

        tool_bar_layout.addWidget(self.tools_widget)
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
