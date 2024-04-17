import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

def zoom_image(image_path, scale):
    app = QApplication(sys.argv)

    # Resmi yükle
    pixmap = QPixmap(image_path)

    # Resmin boyutlarını al
    width = pixmap.width()
    height = pixmap.height()

    # Resmin merkezindeki bölgeyi belirle
    center_x = width // 2
    center_y = height // 2
    region_width = int(width / scale)
    region_height = int(height / scale)
    start_x = max(center_x - region_width // 2, 0)
    end_x = min(center_x + region_width // 2, width)
    start_y = max(center_y - region_height // 2, 0)
    end_y = min(center_y + region_height // 2, height)

    # Belirlenen bölgeyi al
    cropped_pixmap = pixmap.copy(start_x, start_y, end_x - start_x, end_y - start_y)

    # Yeni boyutlara göre resmi ölçeklendir
    scaled_pixmap = cropped_pixmap.scaled(width, height, Qt.KeepAspectRatio)

    # Pencere oluştur
    window = QMainWindow()
    window.setGeometry(100, 100, 800, 600)

    # Etiket oluştur ve resmi etikete yerleştir
    label = QLabel(window)
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter)

    # Ana düzen oluştur
    layout = QVBoxLayout()
    layout.addWidget(label)

    # Ana pencereye ana düzeni yerleştir
    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    # Pencereyi göster
    window.show()

    # Uygulamayı çalıştır
    sys.exit(app.exec_())

# Kullanım örneği
if __name__ == "__main__":
    image_path = "cameraman.png"  # Kullanılacak resmin dosya yolu
    scale = 0.5  # Ölçek değeri
    zoom_image(image_path, scale)
