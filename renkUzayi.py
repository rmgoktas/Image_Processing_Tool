from email.mime import application
import cv2
import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRectF

class RenkUzayiDonusumleriScript(QWidget):

    def convertToRGB(self):
        
        rgb_image = np.zeros_like(self.processed_image)

        #her piksel için renk kanallarını yer değiştiriyoruz
        for y in range(self.processed_image.shape[0]):
            for x in range(self.processed_image.shape[1]):
                b, g, r = self.processed_image[y, x] 
                rgb_image[y, x] = [r, g, b] 

        self.processed_image = rgb_image
        self.showProcessedImage()


    def convertToCMY(self):
            #cmy renk uzayı, bbgr'nin tersi, 255 - bgr 
            cmy_image = 255 - self.processed_image

            self.processed_image = cmy_image
            self.showProcessedImage()


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Renk Uzayı Dönüşümleri')
        self.setFixedSize(1280, 720)

        self.original_image = np.zeros((500, 500, 3), dtype=np.uint8)
        self.processed_image = np.zeros((500, 500, 3), dtype=np.uint8)

        self.label_original = QLabel(self)
        self.label_original.setText("Orijinal Resim")
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_processed = QLabel(self)
        self.label_processed.setText("İşlenmiş Resim")
        self.label_processed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)

        self.button_convert_to_rgb = QPushButton('RGB', self)
        self.button_convert_to_rgb.setEnabled(False)
        self.button_convert_to_rgb.clicked.connect(self.convertToRGB)

        self.button_convert_to_cmy = QPushButton('CMY', self)
        self.button_convert_to_cmy.setEnabled(False)
        self.button_convert_to_cmy.clicked.connect(self.convertToCMY)

        self.button_reset = QPushButton('Resetle', self)
        self.button_reset.setEnabled(False)
        self.button_reset.clicked.connect(self.reset)

        self.button_save_processed = QPushButton('İşlenmiş Resmi Kaydet', self)
        self.button_save_processed.setEnabled(False)
        self.button_save_processed.clicked.connect(self.saveProcessedImage)

        layout_original_content = QVBoxLayout()
        layout_original_content.addWidget(self.label_original)

        layout_original = QHBoxLayout()
        layout_original.addLayout(layout_original_content)

        layout_processed = QVBoxLayout()
        layout_processed.addWidget(self.label_processed)

        layout_images = QHBoxLayout()
        layout_images.addLayout(layout_original)
        layout_images.addLayout(layout_processed)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_convert_to_rgb)
        layout_buttons.addWidget(self.button_convert_to_cmy)

        layout = QVBoxLayout()
        layout.addWidget(self.button_load)
        layout.addLayout(layout_images)
        layout.addLayout(layout_buttons)
        layout.addWidget(self.button_reset)
        layout.addWidget(self.button_save_processed)

        self.setLayout(layout)
        self.show()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Resim Seç', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.original_image = image.copy()
                self.processed_image = image.copy()
                self.showOriginalImage()
                self.showProcessedImage()
                self.enableButtons()

    def showOriginalImage(self):
        label_width = self.label_original.width()
        label_height = self.label_original.height()
        height, width, channel = self.original_image.shape
        bytes_per_line = 3 * width

        pixmap = QPixmap.fromImage(QImage(self.original_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        transparent_pixmap = QPixmap(label_width, label_height)
        transparent_pixmap.fill(Qt.transparent)
        painter = QPainter(transparent_pixmap)
        target_rect = QRectF(0.0, 0.0, label_width, label_height)
        source_rect = QRectF(0.0, 0.0, pixmap.width(), pixmap.height())
        painter.drawPixmap(target_rect, pixmap, source_rect)
        painter.end()

        self.label_original.setPixmap(transparent_pixmap)

    def showProcessedImage(self):
        height, width, channel = self.processed_image.shape
        bytes_per_line = width * channel
        q_image = QImage(self.processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        label_width = self.label_original.width()
        label_height = self.label_original.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label_processed.setPixmap(pixmap)

    def reset(self):
        self.processed_image = self.original_image.copy()  # İşlenmiş resmi orijinal resimle doldur
        self.showProcessedImage()  # İşlenmiş resmi temizleme işlemi için görüntüyü güncelle

    def enableButtons(self):
        self.button_convert_to_rgb.setEnabled(True)
        self.button_convert_to_cmy.setEnabled(True)
        self.button_reset.setEnabled(True)
        self.button_save_processed.setEnabled(True)

    def disableButtons(self):
        self.button_convert_to_rgb.setEnabled(False)
        self.button_convert_to_cmy.setEnabled(False)
        self.button_reset.setEnabled(False)
        self.button_save_processed.setEnabled(False)

    def saveProcessedImage(self):
        if self.processed_image is not None and self.button_save_processed.isEnabled():
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'İşlenmiş Resmi Kaydet', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
            if file_path:
                if not file_path.endswith(('.jpg', '.jpeg', '.png')):
                    file_path += '.jpg' 
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

if __name__ == '__main__':
    app = application(sys.argv)
    ex = RenkUzayiDonusumleriScript()
    sys.exit(app.exec_())
