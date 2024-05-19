import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFileDialog, QPushButton, QScrollBar, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np
import math

class ResimDondurmeScript(QWidget):
    
    def rotateImage(self, angle):
            
            self.rotation_angle = angle

            #trigonometrik islemlerde kullanmak icin açıyı radyan cinsine dönüştür
            radyan = math.radians(angle)

            rows, cols, _ = self.original_image.shape

            center = (cols / 2, rows / 2)

            new_image = np.zeros((rows, cols, 3), dtype=np.uint8)

            for x in range(cols):
                for y in range(rows):

                   #merkezden koordinat cikarma ve sin-cos donusumleri yapilir
                    new_x = int((x - center[0]) * math.cos(radyan) - (y - center[1]) * math.sin(radyan) + center[0])
                    new_y = int((x - center[0]) * math.sin(radyan) + (y - center[1]) * math.cos(radyan) + center[1])

                    #yeni koordinatlar geçerli bir aralıkta ise, orijinal görüntüden pikseli aliyoruz
                    if 0 <= new_x < cols and 0 <= new_y < rows:
                        new_image[y, x, :] = self.original_image[new_y, new_x, :]

            self.processed_image = new_image
            self.showProcessedImage(self.processed_image)
            self.label_rotation_angle.setText(f'Dönme Açısı: {angle}°')  
    
    
    
    
    
    


    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Resim Döndürme')
        self.setFixedSize(1280, 720)

        self.original_image = None
        self.processed_image = None
        self.rotation_angle = 0 

        self.label_original = QLabel(self)
        self.label_processed = QLabel(self)
        self.label_rotation_angle = QLabel(self)  

        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)

        self.scroll_bar = QScrollBar()
        self.scroll_bar.setOrientation(Qt.Horizontal)
        self.scroll_bar.valueChanged.connect(self.rotateImage)

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

        layout_rotation_angle = QHBoxLayout()  
        layout_rotation_angle.addWidget(self.label_rotation_angle, alignment=Qt.AlignRight)  

        layout = QVBoxLayout()
        layout.addWidget(self.button_load)
        layout.addWidget(self.scroll_bar)
        layout.addLayout(layout_images)
        layout.addLayout(layout_rotation_angle)  
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

            self.scroll_bar.setRange(0, 360)
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
        self.original_image = None
        self.processed_image = None
        self.label_original.clear()
        self.label_processed.clear()
        self.label_rotation_angle.clear()
        self.button_save.setEnabled(False)
        self.scroll_bar.setValue(0)

    def saveImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'Resim Kaydet', '', 'JPEG Files (*.jpg);;PNG Files (*.png)')
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))
            QMessageBox.information(self, 'Bilgi', 'İşlenmiş resim başarıyla kaydedildi.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ResimDondurmeScript()
    sys.exit(app.exec_())
