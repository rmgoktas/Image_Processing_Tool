import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class HistogramEqualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Histogram Equalizer")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        
        self.equalize_button = QPushButton("Equalize Histogram", self)
        self.equalize_button.clicked.connect(self.equalize_histogram)
        self.equalize_button.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.equalize_button)
        layout.addWidget(self.image_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_name:
            self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image)
            self.equalize_button.setEnabled(True)

    def display_image(self, img):
        qformat = QImage.Format_Indexed8
        img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.image_label.setPixmap(QPixmap.fromImage(img))
        self.image_label.adjustSize()

    def equalize_histogram(self):
        if self.image is not None:
            equalized_image = self.manual_histogram_equalization(self.image)
            self.display_image(equalized_image)

    def manual_histogram_equalization(self, img):
        # Histogram hesaplama
        hist, bins = np.histogram(img.flatten(), 256, [0,256])

        # Kümülatif dağılım fonksiyonunu hesaplama (CDF)
        cdf = hist.cumsum()

        # CDF'nin minimum değeri (0 olmayan ilk değer)
        cdf_min = cdf[cdf > 0].min()

        # Histogram germe işlemi
        cdf_normalized = (cdf - cdf_min) * 255 / (cdf.max() - cdf_min)
        cdf_normalized = cdf_normalized.astype('uint8')

        # Yeni piksel değerleriyle görüntüyü dönüştürme
        img_equalized = cdf_normalized[img]

        return img_equalized

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistogramEqualizer()
    window.show()
    sys.exit(app.exec_())
