import sys
from PyQt5.QtGui import QImage, QPixmap, qRgb
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QFileDialog
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load grayscale image and color palette
        filename, _ = QFileDialog.getOpenFileName(self, "Open Grayscale Image", "", "Images (*.png *.jpg *.jpeg)")
        if not filename:
            sys.exit()
        self.grayscale_image = QImage(filename)
        self.palette = [
            qRgb(0, 0, 0),
            qRgb(255, 0, 0),
            qRgb(0, 255, 0),
            qRgb(0, 0, 255),
        ]

        # Convert grayscale image to QImage
        self.grayscale_qimage = self.grayscale_image.convertToFormat(QImage.Format_Grayscale8)

        # Create new RGB image and colorize it
        self.colorized_qimage = QImage(self.grayscale_qimage.size(), QImage.Format_RGB32)
        for y in range(self.grayscale_qimage.height()):
            for x in range(self.grayscale_qimage.width()):
                gray_value = self.grayscale_qimage.pixelIndex(x, y)
                color = self.palette[gray_value]
                self.colorized_qimage.setPixelColor(x, y, color)

        # Display the colorized image
        self.label = QLabel(self)
        self.label.setPixmap(QPixmap.fromImage(self.colorized_qimage))
        self.setCentralWidget(self.label)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
