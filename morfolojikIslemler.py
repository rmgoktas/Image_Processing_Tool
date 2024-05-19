import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

class MorfolojikIslemlerScript(QWidget):
    
    def custom_dilate(self, image, kernel_size):
        
        #görüntünün boyutlarını diziye aliyoruz (kac satir kac sutun var??)
        rows, cols = image.shape
        
        #kernel boyutuna gore kenarlara padding ekliyoruz ki kernel bosa dusmesin
        pad_size = kernel_size // 2
        
        #goruntu boyutlarinda sifirlardan olusan matris tanimliyoruz
        dilated_image = np.zeros_like(image)
        
        #tarama
        for i in range(pad_size, rows):
            for j in range(pad_size, cols):
                
                # i ve j icin saga sola, asagi yukari gidip komsu degerleri aliyoruz
                neighborhood = image[i - pad_size: i + pad_size, 
                                     j - pad_size: j + pad_size]
                
                #komsulardan en az biri bile 1 olsa piksel 1 olur
                max_value = np.max(neighborhood)
                
                #uzerinde bulundugumuz pikseli gelen sonuca ayarliyoruz
                dilated_image[i, j] = max_value
        
        return dilated_image


    def custom_erode(self, image, kernel_size):

        rows, cols = image.shape

        pad_size = kernel_size // 2

        eroded_image = np.zeros_like(image)

        for i in range(pad_size, rows):
            for j in range(pad_size, cols):

                neighborhood = image[i - pad_size: i + pad_size, 
                                     j - pad_size: j + pad_size]

                #eger sadece uzerinde bulundugumuz piksel 1 VE tum komsular 1 ise 1 olur
                min_value = np.min(neighborhood)

                eroded_image[i, j] = min_value

        return eroded_image


    def custom_opening(self, image, kernel_size):
        eroded_image = self.custom_erode(image, kernel_size)
        opened_image = self.custom_dilate(eroded_image, kernel_size)
        return opened_image

    def custom_closing(self, image, kernel_size):
        dilated_image = self.custom_dilate(image, kernel_size)
        closed_image = self.custom_erode(dilated_image, kernel_size)
        return closed_image
    
    #fonks
    def dilate(self):
        kernel_size = 3
        original_image_np = self.qimage_to_numpy(self.original_image)
        gray_image = cv2.cvtColor(original_image_np, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.custom_dilate(gray_image, kernel_size)
        self.showProcessedImage()

    def erode(self):
        kernel_size = 3
        original_image_np = self.qimage_to_numpy(self.original_image)
        gray_image = cv2.cvtColor(original_image_np, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.custom_erode(gray_image, kernel_size)
        self.showProcessedImage()

    def opening(self):
        kernel_size = 3
        original_image_np = self.qimage_to_numpy(self.original_image)
        gray_image = cv2.cvtColor(original_image_np, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.custom_opening(gray_image, kernel_size)
        self.showProcessedImage()

    def closing(self):
        kernel_size = 3
        original_image_np = self.qimage_to_numpy(self.original_image)
        gray_image = cv2.cvtColor(original_image_np, cv2.COLOR_BGR2GRAY)
        self.processed_image = self.custom_closing(gray_image, kernel_size)
        self.showProcessedImage()







    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Morfolojik İşlemler')
        self.setFixedSize(1280, 720)

        self.original_image = None
        self.processed_image = None

        self.label_original = QLabel(self)
        self.label_original.setText("Orijinal Resim")
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_processed = QLabel(self)
        self.label_processed.setText("İşlenmiş Resim")
        self.label_processed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)

        self.button_dilate = QPushButton('Genişletme', self)
        self.button_dilate.setEnabled(False)
        self.button_dilate.clicked.connect(self.dilate)

        self.button_erode = QPushButton('Aşınma', self)
        self.button_erode.setEnabled(False)
        self.button_erode.clicked.connect(self.erode)

        self.button_open = QPushButton('Açma', self)
        self.button_open.setEnabled(False)
        self.button_open.clicked.connect(self.opening)

        self.button_close = QPushButton('Kapama', self)
        self.button_close.setEnabled(False)
        self.button_close.clicked.connect(self.closing)

        self.button_save = QPushButton('Kaydet', self)
        self.button_save.setEnabled(False)
        self.button_save.clicked.connect(self.saveImage)

        layout_original = QVBoxLayout()
        layout_original.addWidget(self.label_original)

        layout_processed = QVBoxLayout()
        layout_processed.addWidget(self.label_processed)

        layout_images = QHBoxLayout()
        layout_images.addLayout(layout_original)
        layout_images.addLayout(layout_processed)

        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_load)
        layout_buttons.addWidget(self.button_dilate)
        layout_buttons.addWidget(self.button_erode)
        layout_buttons.addWidget(self.button_open)
        layout_buttons.addWidget(self.button_close)
        layout_buttons.addWidget(self.button_save)

        layout = QVBoxLayout()
        layout.addLayout(layout_images)
        layout.addLayout(layout_buttons)

        self.setLayout(layout)
        self.show()

    def loadImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Resim Seç', '', 'JPEG Files (*.jpg;*.jpeg);;PNG Files (*.png)')
        if file_path:
            image = QImage(file_path)
            if not image.isNull():
                pixmap = QPixmap.fromImage(image)

                self.original_image = image
                self.label_original.setPixmap(pixmap.scaled(self.label_original.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.label_processed.clear()  
                self.enableButtons()  

    def showOriginalImage(self):
        label_width = self.label_original.width()
        label_height = self.label_original.height()
        pixmap = QPixmap.fromImage(self.original_image.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_original.setPixmap(pixmap)

    def showProcessedImage(self):
        label_width = self.label_processed.width()
        label_height = self.label_processed.height()
        processed_image_qimage = self.numpy_to_qimage(self.processed_image)
        pixmap = QPixmap.fromImage(processed_image_qimage.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.label_processed.setPixmap(pixmap)

    def saveImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'İşlenmiş Resmi Kaydet', '', 'JPEG Files (*.jpg);;PNG Files (*.png)')
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

    def enableButtons(self):
        self.button_dilate.setEnabled(True)
        self.button_erode.setEnabled(True)
        self.button_open.setEnabled(True)
        self.button_close.setEnabled(True)
        self.button_save.setEnabled(True)

    def qimage_to_numpy(self, original_image):
        original_image = original_image.convertToFormat(4)
        width = original_image.width()
        height = original_image.height()
        ptr = original_image.bits()
        ptr.setsize(original_image.byteCount())
        arr = np.array(ptr).reshape(height, width, 4) 
        return arr   
    
    def numpy_to_qimage(self, image_np):
        if len(image_np.shape) == 2:  
            height, width = image_np.shape
            bytesPerLine = width
            return QImage(image_np.data, width, height, bytesPerLine, QImage.Format_Grayscale8)
        
    def saveImage(self):
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getSaveFileName(self, 'Resim Kaydet', '', 'JPEG Files (*.jpg);;PNG Files (*.png)')
            if file_path:
                cv2.imwrite(file_path, self.processed_image)
                QMessageBox.information(self, 'Bilgi', 'İşlenmiş resim başarıyla kaydedildi.', QMessageBox.Ok)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MorfolojikIslemlerScript()
    sys.exit(app.exec_())
