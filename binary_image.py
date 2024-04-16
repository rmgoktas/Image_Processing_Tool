import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
import cv2
from PyQt5.QtCore import Qt

def binaryimage(img):
    if img is None:
        print("Resim yüklenemedi.")
        return None
    else:
        height, width = img.shape[:2]
        binaryimg = np.zeros((height, width), dtype=np.uint8)
        for y in range(height):
            for x in range(width):
                pixel = img[y, x]
                if (pixel < 128).any():
                    binaryimg[y, x] = 0
                else:
                    binaryimg[y, x] = 255
        return binaryimg

def bgr_to_qpixmap(bgr_image):
    qimage = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
    height, width, channel = qimage.shape
    bytesPerLine = 3 * width
    qImg = QImage(qimage.data, width, height, bytesPerLine, QImage.Format_RGB888)
    return QPixmap.fromImage(qImg)

class ImageProcessingApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Binary Image')
        self.setGeometry(150, 150, 1200, 800)
        
        self.image_label = QLabel(self)
        self.image_label.setGeometry(50, 100, 400, 400)
        
        open_image_button = QPushButton("Resim Seç", self)
        open_image_button.setGeometry(50, 50, 400, 30)
        open_image_button.clicked.connect(self.selectimage)
        
        start_button = QPushButton("İşlemi Başlat", self)
        start_button.setGeometry(50, 525, 400, 30)
        start_button.clicked.connect(self.showimg)
        
        self.image_path = ""
        self.processed_image_label = QLabel(self)
        self.processed_image_label.setGeometry(500, 100, 400, 400)

def selectimage(self):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Resim Seç", "", "Resim Dosyalar (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
    if file_path:
        self.image_path = file_path
        pixmap = QPixmap(file_path)
        pixmap_scaled = pixmap.scaled(self.image_label.size(), aspectRatioMode=Qt.KeepAspectRatio)
        self.image_label.setPixmap(pixmap_scaled)

    def showimg(self):
        if self.image_path:
            img = cv2.imread(self.image_path)

            binaryimg = binaryimage(img)
            if binaryimg is not None:
                qImg = bgr_to_qpixmap(binaryimg)
                self.processed_image_label.setPixmap(qImg)
        else:
            print("Lütfen bir resim seçin.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessingApp()
    ex.show()
    sys.exit(app.exec_())
