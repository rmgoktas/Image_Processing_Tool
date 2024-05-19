import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QScrollBar, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import cv2
import numpy as np

class ParlaklikArtirmaAzaltmaScript(QWidget):

    def increaseBrightness(self, brightness_level):
        
        self.brightness_level = brightness_level 
        
        brightness_percentage = int(brightness_level * 100 / 255)
        
        #brightness_level degerini orijinal resme ekle
        self.processed_image = np.clip(self.original_image.astype(int) + brightness_level, 0, 255).astype(np.uint8)
        
        self.showProcessedImage(self.processed_image)
        self.label_brightness_level.setText(f'Parlaklık Seviyesi: {brightness_percentage}%')


    

    
    
    
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Parlaklık Artırma')
        self.setFixedSize(1280, 720)

        self.original_image = None
        self.processed_image = None
        self.brightness_level = 0  

        self.label_original = QLabel(self)
        self.label_processed = QLabel(self)
        self.label_brightness_level = QLabel(self)  

        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)

        self.scroll_bar = QScrollBar()
        self.scroll_bar.setOrientation(Qt.Horizontal)
        self.scroll_bar.setMinimum(0)  
        self.scroll_bar.setMaximum(255)   
        self.scroll_bar.setValue(0) 

        self.scroll_bar.valueChanged.connect(self.increaseBrightness)

        self.button_reset = QPushButton('Resetle', self)
        self.button_reset.clicked.connect(self.resetImage)

        self.button_save = QPushButton('İşlenmiş Resmi Kaydet', self)
        self.button_save.setEnabled(False)
        self.button_save.clicked.connect(self.saveImage)

        layout_original = QVBoxLayout()
        layout_original.addWidget(QLabel('Orijinal Resim'))
        layout_original.addWidget(self.label_original)

        layout_processed = QVBoxLayout()
        layout_processed.addWidget(QLabel('İşlenmiş Resim'))
        layout_processed.addWidget(self.label_processed)

        layout_images = QHBoxLayout()
        layout_images.addLayout(layout_original)
        layout_images.addLayout(layout_processed)

        layout_brightness_level = QHBoxLayout() 
        layout_brightness_level.addWidget(self.label_brightness_level, alignment=Qt.AlignRight) 

        layout = QVBoxLayout()
        layout.addWidget(self.button_load)
        layout.addWidget(self.scroll_bar)
        layout.addLayout(layout_images)
        layout.addLayout(layout_brightness_level) 
        layout.addWidget(self.button_reset) 
        layout.addWidget(self.button_save)

        self.setLayout(layout)
        self.show()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Resim Seç', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
        if file_path:
            image = cv2.imread(file_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            self.original_image = image.copy()
            self.processed_image = image.copy()
            self.showOriginalImage(self.original_image)
            self.showProcessedImage(self.processed_image)

            self.scroll_bar.setValue(0)  
            self.button_save.setEnabled(True)

    def showOriginalImage(self, image):
        label_width = int(self.label_original.width() * 1.9)
        label_height = int(self.label_original.height() * 1.9)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_original.setPixmap(pixmap)

    def showProcessedImage(self, image):
        label_width = int(self.label_original.width() * 1.9)
        label_height = int(self.label_original.height() * 1.9)
        height, width, channel = image.shape
        bytes_per_line = 3 * width
        q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label_processed.setPixmap(pixmap)

    def resetImage(self):
        self.processed_image = None
        self.label_brightness_level.clear()
        self.scroll_bar.setValue(0)  

    def saveImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Resim Kaydet', '', 'JPEG Files (*.jpg);;PNG Files (*.png)')
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))
            QMessageBox.information(self, 'Bilgi', 'İşlenmiş resim başarıyla kaydedildi.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ParlaklikArtirmaAzaltmaScript()
    sys.exit(app.exec_())
