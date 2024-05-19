import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class NoiseReductionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Noise Reduction")
        self.setGeometry(100, 100, 800, 600)
        
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        
        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)
        
        self.add_noise_button = QPushButton("Add Salt & Pepper Noise", self)
        self.add_noise_button.clicked.connect(self.add_noise)
        self.add_noise_button.setEnabled(False)
        
        self.mean_filter_button = QPushButton("Apply Mean Filter", self)
        self.mean_filter_button.clicked.connect(self.apply_mean_filter)
        self.mean_filter_button.setEnabled(False)
        
        self.median_filter_button = QPushButton("Apply Median Filter", self)
        self.median_filter_button.clicked.connect(self.apply_median_filter)
        self.median_filter_button.setEnabled(False)
        
        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.add_noise_button)
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.mean_filter_button)
        filter_layout.addWidget(self.median_filter_button)
        
        layout.addLayout(filter_layout)
        layout.addWidget(self.image_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.image = None
        self.noisy_image = None

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp)", options=options)
        if file_name:
            self.image = cv2.imread(file_name, cv2.IMREAD_GRAYSCALE)
            self.display_image(self.image)
            self.add_noise_button.setEnabled(True)

    def display_image(self, img):
        height, width = img.shape
        bytes_per_line = width
        qimg = QImage(img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        self.image_label.setPixmap(QPixmap.fromImage(qimg))
        self.image_label.adjustSize()

    def add_noise(self):
        if self.image is not None:
            self.noisy_image = self.salt_and_pepper_noise(self.image)
            self.display_image(self.noisy_image)
            self.mean_filter_button.setEnabled(True)
            self.median_filter_button.setEnabled(True)

    def salt_and_pepper_noise(self, image, salt_prob=0.02, pepper_prob=0.02):
        noisy_img = np.copy(image)
        total_pixels = image.size

        # Salt noise
        num_salt = int(total_pixels * salt_prob)
        coords = [np.random.randint(0, i, num_salt) for i in image.shape]
        noisy_img[coords[0], coords[1]] = 255

        # Pepper noise
        num_pepper = int(total_pixels * pepper_prob)
        coords = [np.random.randint(0, i, num_pepper) for i in image.shape]
        noisy_img[coords[0], coords[1]] = 0

        return noisy_img

    def apply_mean_filter(self):
        if self.noisy_image is not None:
            filtered_image = self.mean_filter(self.noisy_image)
            self.display_image(filtered_image)

    def mean_filter(self, image, kernel_size=3):
        pad_size = kernel_size // 2
        padded_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        filtered_image = np.zeros_like(image)

        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                region = padded_image[y:y + kernel_size, x:x + kernel_size]
                filtered_image[y, x] = np.mean(region)

        return filtered_image

    def apply_median_filter(self):
        if self.noisy_image is not None:
            filtered_image = self.median_filter(self.noisy_image)
            self.display_image(filtered_image)

    def median_filter(self, image, kernel_size=3):
        pad_size = kernel_size // 2
        padded_image = np.pad(image, pad_size, mode='constant', constant_values=0)
        filtered_image = np.zeros_like(image)

        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                region = padded_image[y:y + kernel_size, x:x + kernel_size]
                filtered_image[y, x] = np.median(region)

        return filtered_image

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NoiseReductionApp()
    window.show()
    sys.exit(app.exec_())
