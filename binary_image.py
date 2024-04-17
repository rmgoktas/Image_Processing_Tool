import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PIL import Image

def binary_image(img):
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

class ImageProcessor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Resim İşleyici")
        self.setGeometry(100, 100, 1200, 800)  # Ekran boyutunu artırdık

        self.label = QLabel(self)
        self.label.setGeometry(50, 50, 400, 400)  # Etiket boyutunu artırdık

        self.select_button = QPushButton("Resim Seç", self)
        self.select_button.setGeometry(50, 50, 150, 30)  # Butonun konumunu değiştirdik
        self.select_button.clicked.connect(self.select_image)

        self.process_button = QPushButton("İşle ve Göster", self)
        self.process_button.setGeometry(50, 500, 150, 30)  # Butonun konumunu değiştirdik
        self.process_button.clicked.connect(self.process_and_show_image)

        self.selected_image_path = None  # Seçilen resmin yolunu tutmak için bir değişken

    def show_image(self):
        if self.selected_image_path:
            image = Image.open(self.selected_image_path)
            image_array = np.array(image)  # PIL Image'ı numpy dizisine dönüştür
            if image_array is not None:
                height, width = image_array.shape[:2]
                q_image = QImage(image_array, width, height, QImage.Format_Grayscale8)  # QImage'e dönüştür
                
                # Eğer resim ekrandan büyükse, boyutunu değiştir
                max_width = 500
                max_height = 300
                if width > max_width or height > max_height:
                    q_image = q_image.scaled(max_width, max_height, aspectRatioMode=True)
                
                pixmap = QPixmap.fromImage(q_image)  # QPixmap'a dönüştür
                self.label.setPixmap(pixmap)  # Etikete resmi yerleştir
    
    
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Resim Seç", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.selected_image_path = file_path  # Seçilen resmin yolunu değişkende sakla
            # Seçilen resmi ilk başta göster
            image = Image.open(self.selected_image_path)
            q_image = QImage(image.tobytes(), image.width, image.height, QImage.Format_RGB888)  # QImage'e dönüştürüyoruz
            pixmap = QPixmap.fromImage(q_image)  # QPixmap'a dönüştürüyoruz
            self.label.setPixmap(pixmap)
        

    def process_and_show_image(self):
        if self.selected_image_path:
            image = Image.open(self.selected_image_path)
            image_array = np.array(image)  # PIL Image'ı numpy dizisine dönüştür
            binary_img = binary_image(image_array)  # İşlevi kullanarak resmi işle
            if binary_img is not None:
                height, width = binary_img.shape[:2]
                q_image = QImage(binary_img, width, height, QImage.Format_Grayscale8)  # QImage'e dönüştür
                
                # Eğer resim ekrandan büyükse, boyutunu değiştir
                max_width = 500
                max_height = 300
                if width > max_width or height > max_height:
                    q_image = q_image.scaled(max_width, max_height, aspectRatioMode=True)
                
                pixmap = QPixmap.fromImage(q_image)  # QPixmap'a dönüştür
                self.label.setPixmap(pixmap)  # Etikete resmi yerleştir

    
    
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())
