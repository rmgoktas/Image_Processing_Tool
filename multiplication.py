import sys
from tkinter import Image
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog,QWidget,QSizePolicy,QHBoxLayout,QVBoxLayout
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRectF
import cv2

def multiplication(img1,img2):
    img1height,img1width,img1ch=img1.shape
    img2height,img2width,img2ch=img2.shape
    
    if((img1height==img2height)&(img1width==img2width)&(img1ch==img2ch)):
        
        if(img1ch==1):
            newimg=np.zeros((img1height,img1width),dtype=np.uint8)
            
            for y in range(img1height):
                for x in range(img1width):
                    img1_pixel_value=img1[y,x]
                    img2_pixel_value=img2[y,x]
                    new_value=img1_pixel_value*img2_pixel_value
                    if(new_value>255):
                        newimg[y,x]=255
                    else:
                        newimg[y,x]=new_value
            return newimg
        else:
            newimg=np.zeros((img1height,img1width,3),dtype=np.uint8)
            
            for y in range(img1height):
                for x in range(img1width):
                    img1_blue=img1[y,x,0]
                    img2_blue=img2[y,x,0]
                    blue_value=img1_blue*img2_blue
                    if(blue_value>255):
                        newimg[y,x,0]=255
                    else:
                        newimg[y,x,0]=blue_value
                    img1_green=img1[y,x,1]
                    img2_green=img2[y,x,1]
                    green_Value=img1_green*img2_green
                    if(green_Value>255):
                        newimg[y,x,1]=255
                    else:
                        newimg[y,x,1]=green_Value
                    img1_red=img1[y,x,2]
                    img2_red=img2[y,x,2]
                    red_value=img1_red*img2_red
                    if(red_value>255):
                        newimg[y,x,2]=255
                    else:
                        newimg[y,x,2]=red_value
            return newimg
    else:
        print("Resimler ayni boyutta veya formatta degil")



class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Resim Çarpma')
        self.setFixedSize(1280, 720)

        # Orijinal resim ve işlenmiş resim değişkenleri
        self.original_image = np.zeros((300, 300, 3), dtype=np.uint8)
        self.original_image1 = np.zeros((300, 300, 3), dtype=np.uint8)
        self.processed_image = np.zeros((300, 300, 3), dtype=np.uint8)

        # Orijinal resim ve işlenmiş resim için etiketler oluştur
        self.label_original = QLabel(self)
        self.label_original.setText("Orijinal Resim")
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #ek resim
        self.label_original1 = QLabel(self)
        self.label_original1.setText("Orijinal Resim")
        self.label_original1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.label_processed = QLabel(self)
        self.label_processed.setText("İşlenmiş Resim")
        self.label_processed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Resim yükleme düğmesi oluştur
        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)
        
        # Ek düğme oluştur
        self.button_load2 = QPushButton('Resim Yükle2', self)
        self.button_load2.clicked.connect(self.loadImage2)


        # Resetleme düğmesini oluştur
        self.button_reset = QPushButton('Resetle', self)
        self.button_reset.setEnabled(False)
        self.button_reset.clicked.connect(self.reset)

        self.button_save_processed = QPushButton('İşlenmiş Resmi Kaydet', self)
        self.button_save_processed.setEnabled(False)
        self.button_save_processed.clicked.connect(self.saveProcessedImage)

        

        # Orijinal resim ve etiketini bir düzende topla
        layout_original_content = QVBoxLayout()
        layout_original_content.addWidget(self.label_original)
        
        #ekresim
        layout_original1_content = QVBoxLayout()
        layout_original1_content.addWidget(self.label_original1)

        # Orijinal resim ve etiketi düzene ekle
        layout_original = QHBoxLayout()
        layout_original.addLayout(layout_original_content)
        #ekresim
        layout_original1 = QHBoxLayout()
        layout_original1.addLayout(layout_original1_content)
        
        layout_processed = QVBoxLayout()
        layout_processed.addWidget(self.label_processed)

        layout_images = QHBoxLayout()
        layout_images.addLayout(layout_original)
        layout_images.addLayout(layout_original1)
        layout_images.addLayout(layout_processed)

        layout_buttons = QHBoxLayout()


        # Ana düzeni oluştur
        layout = QVBoxLayout()
        layout.addWidget(self.button_load)
        layout.addWidget(self.button_load2)
        layout.addLayout(layout_images)
        layout.addLayout(layout_buttons)
        layout.addWidget(self.button_reset)
        layout.addWidget(self.button_save_processed)

        self.setLayout(layout)
        self.show()

    # Resim yükleme işlevi
    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Resim Seç', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.original_image = image.copy()
                self.original_image1 = image.copy()
                self.showOriginalImage()
                
                self.enableButtons()
    def loadImage2(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Resim Seç', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
        if file_path:
            image = cv2.imread(file_path)
            if image is not None:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                self.original1_image1 = image.copy()
                self.showOriginalImage1()  # İkinci resmi göster
                self.showProcessedImage()
                self.enableButtons()

    def showOriginalImage(self):
        label_width = self.label_original.width()
        label_height = self.label_original.height()
        height, width, channel = self.original_image.shape
        bytes_per_line = 3 * width

        # Orijinal resmi boyutlandır
        pixmap = QPixmap.fromImage(QImage(self.original_image.data, width, height, bytes_per_line, QImage.Format_RGB888))

        # Orijinal pixmap'i etiket boyutuna dönüştür
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Orijinal resmi göster
        self.label_original.setPixmap(pixmap)
        
    def showOriginalImage1(self):
        label_width = self.label_original1.width()
        label_height = self.label_original1.height()
        height, width, channel = self.original_image1.shape
        bytes_per_line = 3 * width

        # Orijinal resmi boyutlandır
        pixmap = QPixmap.fromImage(QImage(self.original_image1.data, width, height, bytes_per_line, QImage.Format_RGB888))

        # Orijinal pixmap'i etiket boyutuna dönüştür
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Orijinal resmi göster
        self.label_original1.setPixmap(pixmap)
        
    # İşlenmiş resmi gösterme işlevi
    def showProcessedImage(self):
        if self.original_image is not None and self.original_image1 is not None:
            
            proimg = multiplication(self.original_image1, self.original_image)
            
            height, width, channel = proimg.shape  # Kanalları al
            
            # NumPy dizisini QImage'e dönüştür
            q_image = QImage(proimg.data, width, height, channel * width, QImage.Format_RGB888)
            
            # QPixmap oluştur ve QLabel'e ekle
            pixmap = QPixmap.fromImage(q_image)

            label_width = self.label_original.width()
            label_height = self.label_original.height()
            pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.label_processed.setPixmap(pixmap)
        else:
            print("İşlenmiş resim bulunamadi.") 

    # Resetleme işlevi
    def reset(self):
        self.processed_image = None
        self.label_processed.clear()

    # Düğmeleri etkinleştirme işlevi
    def enableButtons(self):
        self.button_reset.setEnabled(True)
        self.button_save_processed.setEnabled(True)

    def disableButtons(self):
        self.button_reset.setEnabled(False)
        self.button_save_processed.setEnabled(False)


    # İşlenmiş resmi kaydetme işlevi
    def saveProcessedImage(self):
        if self.processed_image is not None and self.button_save_processed.isEnabled():
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'İşlenmiş Resmi Kaydet', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
            if file_path:
                # Dosya uzantısını kontrol et
                if not file_path.endswith(('.jpg', '.jpeg', '.png')):
                    file_path += '.jpg'  # Varsayılan olarak JPEG uzantısı ekleyin
                cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())