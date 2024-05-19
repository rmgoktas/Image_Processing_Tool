import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class KenarBulmaScript(QWidget):
    

    def calculate_gradients(self, image):
        
        #goruntuyu gray level'a ceviriyoruz.
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        #sobel filtrelerini tanimliyoruz
        sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], dtype=np.float32)
        sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=np.float32)

        #gradyanlari elde etmek icin goruntu, derinlik ve filtre kullaniyoruz
        grad_x = cv2.filter2D(gray_image, -1, sobel_x)
        grad_y = cv2.filter2D(gray_image, -1, sobel_y)

        #gradyanlari topluyoruz ve her pikseldeki toplam gradyan degerini iceren goruntuyu elde ediyoruz
        edges=np.add(grad_x,grad_y)

        return edges

    def detectEdges(self):
        
        edges = self.calculate_gradients(self.original_image)

        self.processed_image = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
        self.showProcessedImage()
        self.enableSaveButton()   

    

    
    


    def __init__(self):
        super().__init__()
        self.initUI() 

    def initUI(self):
        self.setWindowTitle('Kenar Tespiti')
        self.setFixedSize(1280, 720)
  
        self.original_image = np.zeros((500, 500, 3), dtype=np.uint8)
        self.processed_image = np.zeros((500, 500, 3), dtype=np.uint8)
      
        self.label_original = QLabel(self)
        self.label_original.setText("Orijinal Resim")
        self.label_original.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label_processed = QLabel(self)
        self.label_processed.setText("Kenarlar")
        self.label_processed.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
      
        self.button_load = QPushButton('Resim Yükle', self)
        self.button_load.clicked.connect(self.loadImage)
        self.button_load.setGeometry(20,20,100,20)
       
        self.button_detect_edges = QPushButton('Kenarları Bul', self)
        self.button_detect_edges.setEnabled(False)
        self.button_detect_edges.clicked.connect(self.detectEdges)
      
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
        layout_buttons.addWidget(self.button_load)
        layout_buttons.addWidget(self.button_detect_edges)
        layout_buttons.addWidget(self.button_reset)
        layout_buttons.addWidget(self.button_save_processed)

        layout = QVBoxLayout()
        layout.addLayout(layout_images)
        layout.addLayout(layout_buttons)

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
                self.enableButtons()

    def showOriginalImage(self):
        label_width = self.label_original.width()
        label_height = self.label_original.height()
        height, width, channel = self.original_image.shape
        bytes_per_line = 3 * width

        pixmap = QPixmap.fromImage(QImage(self.original_image.data, width, height, bytes_per_line, QImage.Format_RGB888))
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label_original.setPixmap(pixmap)

    def showProcessedImage(self):
        height, width, channel = self.processed_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(self.processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)

        label_width = self.label_original.width()
        label_height = self.label_original.height()
        pixmap = pixmap.scaled(label_width, label_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.label_processed.setPixmap(pixmap)

    def saveProcessedImage(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(self, 'İşlenmiş Resmi Kaydet', '', 'JPEG Files (*.jpg);;PNG Files (*.png)')
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR))

    def reset(self):
        self.processed_image = None
        self.label_processed.clear()
        self.disableSaveButton()

    def enableButtons(self):
        self.button_detect_edges.setEnabled(True)
        self.button_reset.setEnabled(True)

    def enableSaveButton(self):
        self.button_save_processed.setEnabled(True)

    def disableSaveButton(self):
        self.button_save_processed.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = KenarBulmaScript()
    sys.exit(app.exec_())
