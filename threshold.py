import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRectF
import cv2

def threshold(img,maxvalue,adaptivetype,blocksize):
    
    height,width=img.shape[:2]
    
    blocks = []
    if(adaptivetype==1):
        new_img=np.zeros((height,width),dtype=np.uint8)
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                blocks.append(block) 
        
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                mean_value=mean(block)
                
                for k in range(block.shape[0]):
                    for l in range(block.shape[1]):
                        if(block[k,l]<mean_value/2):
                            block[k,l]=0
                        else:
                            block[k,l]=maxvalue
                new_img[y:y+blocksize, x:x+blocksize] = block
        return new_img      
    if(adaptivetype==2):
        new_img=np.zeros((height,width),dtype=np.uint8)
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                blocks.append(block) 
        
        for y in range(0,height,blocksize):
            for x in range(0,height,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                mean_value=mean(block)
                
                for k in range(block.shape[0]):
                    for l in range(block.shape[1]):
                        if(block[k,l]<mean_value/2):
                            block[k,l]=maxvalue
                        else:
                            block[k,l]=0
                new_img[y:y+blocksize, x:x+blocksize] = block
        return new_img
           
def mean(block):
    if len(block.shape) == 2:  # Blok 2 boyutlu bir dizi mi?
        height, width = block.shape
        total_value = 0
        
        for y in range(height):
            for x in range(width):
                total_value += block[y, x]
        
        mean_value = total_value / (height * width)
        
        return mean_value
    else:
        raise ValueError("Block, beklenen 2 boyutlu bir dizi değil.")

    
    

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Threshold')
        self.setFixedSize(1280, 720)

        # Orijinal resim ve işlenmiş resim değişkenleri
        self.original_image = np.zeros((500, 500, 3), dtype=np.uint8)
        self.processed_image = np.zeros((500, 500, 3), dtype=np.uint8)

        # Orijinal resim ve işlenmiş resim için etiketler oluştur
        self.label_original = QLabel(self)
        self.label_original.setText("Orijinal Resim")
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_processed = QLabel(self)
        self.label_processed.setText("İşlenmiş Resim")
        self.label_processed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Resim yükleme düğmesi oluştur
        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)



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

        # Orijinal resim ve etiketi düzene ekle
        layout_original = QHBoxLayout()
        layout_original.addLayout(layout_original_content)

        layout_processed = QVBoxLayout()
        layout_processed.addWidget(self.label_processed)

        layout_images = QHBoxLayout()
        layout_images.addLayout(layout_original)
        layout_images.addLayout(layout_processed)

        layout_buttons = QHBoxLayout()


        # Ana düzeni oluştur
        layout = QVBoxLayout()
        layout.addWidget(self.button_load)
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
                self.processed_image = image.copy()
                self.showOriginalImage()
                self.showProcessedImage()
                self.enableButtons()

    def showOriginalImage(self):
        label_width = self.label_original.width()
        label_height = self.label_original.height()
        height, width, channel = self.original_image.shape
        bytes_per_line = 3 * width

        # Orijinal resmi boyutlandır
        pixmap = QPixmap.fromImage(QImage(self.original_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Saydam bir pixmap oluştur ve içine resmi yerleştir
        transparent_pixmap = QPixmap(label_width, label_height)
        transparent_pixmap.fill(Qt.transparent)
        painter = QPainter(transparent_pixmap)
        target_rect = QRectF(0.0, 0.0, label_width, label_height)
        source_rect = QRectF(0.0, 0.0, pixmap.width(), pixmap.height())
        painter.drawPixmap(target_rect, pixmap, source_rect)
        painter.end()

        # Orijinal resmi göster
        self.label_original.setPixmap(transparent_pixmap)

    # İşlenmiş resmi gösterme işlevi
    def showProcessedImage(self):
        if self.processed_image is not None:
            img=cv2.cvtColor(self.original_image,cv2.COLOR_BGR2GRAY)
            binary_img = threshold(img, maxvalue=255, adaptivetype=1, blocksize=10)  # Resmi binary hale getir
            self.processed_image=binary_img
            height, width = binary_img.shape
            bytes_per_line = width
            q_image = QImage(binary_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # Resize the processed pixmap to match the size of the original image
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







