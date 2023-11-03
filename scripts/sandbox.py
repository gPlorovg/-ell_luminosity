import sys
from PyQt5 import QtGui, QtWidgets


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 100)
        self.setWindowTitle("ProgressBar")
        self.setWindowIcon(QtGui.QIcon.fromTheme('python3'))
        self.statusBar().showMessage("Ready", 0)

        self.btn = QtWidgets.QPushButton("Download", self)
        self.btn.move(10, 10)
        self.btn.clicked.connect(self.download)
        self.progress_bar = QtWidgets.QProgressBar()
        self.statusBar().addPermanentWidget(self.progress_bar)
        self.progress_bar.hide()

    def download(self):
        self.completed = 0
        self.progress_bar.setFixedSize(self.geometry().width() - 120, 16)
        self.progress_bar.show()
        self.statusBar().showMessage("downloading ...", 0)

        while self.completed < 100:
            self.completed += 0.00005
            self.progress_bar.setValue(int(self.completed))

            if self.progress_bar.value() == 100:
                self.statusBar().showMessage("completed", 0)
                self.progress_bar.hide()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())