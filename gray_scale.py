import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.image_path = None
        self.original_image = None
        self.displayed_image = None

        self.setWindowTitle("Resim Gri Dönüşüm Uygulaması")
        self.setGeometry(100, 100, 640, 480)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        self.convert_button = QPushButton("Griye Dönüştür", self)
        self.convert_button.clicked.connect(self.convert_to_gray)

        self.open_button = QPushButton("Resim Aç", self)
        self.open_button.clicked.connect(self.open_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.convert_button)
        layout.addWidget(self.open_button)

        self.central_widget.setLayout(layout)

    def open_image(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Resim Aç", "", "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if filename:
            self.image_path = filename
            self.original_image = cv2.imread(self.image_path)
            self.display_image()

    def display_image(self):
        if self.original_image is not None:
            height, width, channel = self.original_image.shape
            bytesPerLine = 3 * width
            qImg = QImage(self.original_image.data, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qImg)
            self.image_label.setPixmap(pixmap.scaled(400, 300, Qt.KeepAspectRatio))

    def convert_to_gray(self):
        if self.original_image is not None:
            gray_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
            self.displayed_image = cv2.cvtColor(gray_image, cv2.COLOR_GRAY2BGR)
            self.display_image()
            self.original_image = self.displayed_image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
