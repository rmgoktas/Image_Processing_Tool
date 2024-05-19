import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ConvolutionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gaussian Convolution")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        
        self.convolve_button = QPushButton("Apply Gaussian Convolution", self)
        self.convolve_button.clicked.connect(self.apply_convolution)
        self.convolve_button.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.convolve_button)
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
            self.convolve_button.setEnabled(True)

    def display_image(self, img):
        qformat = QImage.Format_Indexed8
        img = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        self.image_label.setPixmap(QPixmap.fromImage(img))
        self.image_label.adjustSize()

    def apply_convolution(self):
        if self.image is not None:
            kernel_size = 11
            sigma = 1.0
            gaussian_kernel = self.create_gaussian_kernel(kernel_size, sigma)
            convolved_image = self.manual_convolution(self.image, gaussian_kernel)
            self.display_image(convolved_image)

    def create_gaussian_kernel(self, size, sigma):
        kernel = np.fromfunction(
            lambda x, y: (1/ (2 * np.pi * sigma**2)) * np.exp(-((x - (size - 1) / 2)**2 + (y - (size - 1) / 2)**2) / (2 * sigma**2)),
            (size, size)
        )
        return kernel / np.sum(kernel)

    def manual_convolution(self, img, kernel):
        k_height, k_width = kernel.shape
        pad_height = k_height // 2
        pad_width = k_width // 2

        padded_img = np.pad(img, ((pad_height, pad_height), (pad_width, pad_width)), mode='constant')
        convolved_img = np.zeros_like(img)

        for y in range(img.shape[0]):
            for x in range(img.shape[1]):
                convolved_img[y, x] = np.sum(kernel * padded_img[y:y + k_height, x:x + k_width])

        convolved_img = np.clip(convolved_img, 0, 255)
        return convolved_img.astype(np.uint8)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConvolutionApp()
    window.show()
    sys.exit(app.exec_())
