import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout, QSlider
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QRectF
import cv2

def resize_image(img, scale, center=None):
    
    if scale<1:
        # Eski boyutları al
        height, width = img.shape[:2]
        # Yeni boyutu al
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Yeni boş bir görüntü oluştur
        resized_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        
        # Boyut oranlarını hesapla
        width_ratio = width / new_width
        height_ratio = height / new_height
        
        # Yeniden boyutlandırma işlemi
        for y in range(new_height):
            for x in range(new_width):
                resized_x = int(x * width_ratio)
                resized_y = int(y * height_ratio)
                # Eğer orijinal koordinatlar resmin içindeyse, yeniden boyutlandırılmış resme atama yap
                if resized_x < width and resized_y < height:
                    resized_img[y, x] = img[resized_y, resized_x]
                else:
                    # Dışarı taşan pikselleri siyahlaştır
                    resized_img[y, x] = [0, 0, 0]
        
        return resized_img
    else:
        # Eski boyutları al
        height, width = img.shape[:2]
        # Yeni boyutu al
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Yeni boş bir görüntü oluştur
        zoomed_img = np.zeros((new_height, new_width, 3), dtype=np.uint8)
        
        # Boyut oranlarını hesapla
        width_ratio = width / new_width
        height_ratio = height / new_height
        
        # Yakınlaştırma işlemi
        for y in range(new_height):
            for x in range(new_width):
                original_x = int(x * width_ratio)
                original_y = int(y * height_ratio)
                # Eğer orijinal koordinatlar resmin içindeyse, yakınlaştırılmış resme atama yap
                if original_x < width and original_y < height:
                    zoomed_img[y, x] = img[original_y, original_x]
        
        return zoomed_img
    
    
    




class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Binary Dönüşüm')
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

        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setGeometry(50, 50, 1180, 20)
        self.slider.setRange(1, 500)  # Minimum ve maksimum değer aralığını belirle
        self.slider.setValue(100)  # Başlangıç değerini belirle
        self.slider.setSingleStep(1)  # Tek adımda kaydırma miktarını belirle
        self.slider.valueChanged.connect(self.on_slider_changed)  # Slider değeri değiştiğinde işlevi bağla

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
        layout.addWidget(self.slider)
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

        # Orijinal resmi uygun boyuta ölçeklendir
        pixmap = QPixmap.fromImage(QImage(self.original_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        # Orijinal resmi göster
        self.label_original.setPixmap(pixmap)


    # İşlenmiş resmi gösterme işlevi
    def showProcessedImage(self):
        if self.processed_image is not None:
            scale_factor = self.slider.value() / 100.0
            
            # Orta noktayı al
            center_x = self.original_image.shape[1] / 2
            center_y = self.original_image.shape[0] / 2
            
            # Ölçek faktörünü hesapla
            scale = scale_factor
            resize_img = resize_image(self.original_image, scale)
            self.processed_image = resize_img
            
            height, width, channel = resize_img.shape
            bytes_per_line = 3 * width
            q_image = QImage(resize_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)

            # QLabel'da resmi merkezlemek için gerekli boşlukları hesapla
            label_width = self.label_original.width()
            label_height = self.label_original.height()
            x_offset = (label_width - width) / 2
            y_offset = (label_height - height) / 2

            # QLabel'a pixmap'i yerleştir
            painter = QPainter(pixmap)
            painter.drawPixmap(int(x_offset), int(y_offset), pixmap)
            painter.end()

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

    # Slider değeri değiştiğinde çağrılan işlev
    def on_slider_changed(self):
        self.showProcessedImage()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageProcessor()
    window.show()
    sys.exit(app.exec_())

