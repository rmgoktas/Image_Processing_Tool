from curses import window
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFileDialog,QListWidget,QComboBox
from PyQt5.QtGui import QPixmap
file_path=None
def main():
    # Uygulama objesini oluştur
    app = QApplication(sys.argv)
    
    # Ana pencereyi oluştur
    window = QWidget()
    window.setWindowTitle('PyQt5 Pencere Örneği')
    window.setGeometry(150, 150, 1200, 800)  # (x, y, width, height)
    
    # Resim etiketi
    image_label = QLabel(window)
    image_label.setGeometry(50, 80, 300, 300)
    
    # Resim seçme butonu
    open_image_button = QPushButton("Resim Seç", window)
    open_image_button.setGeometry(50, 50, 100, 30)
    open_image_button.clicked.connect(lambda: select_image(image_label))
    
    # Resim seçme butonu
    startbutton = QPushButton("start", window)
    startbutton.setGeometry(80, 400, 100, 30)

    # Seçenekler listesi
    options_list = ["Binary Dönüşüm", "Zoom", "Topla","Çarp","Adaptif Eşikleme","Blurlama"]
    combo_box = QComboBox(window)
    combo_box.setGeometry(50, 400, 200, 30)
    combo_box.addItems(options_list)
    # Pencereyi göster
    window.show()
    
    # Uygulamayı çalıştır
    sys.exit(app.exec_())
    
def showimage(img):
    pixmap = QLabel(window)
    pixmap.setPixmap(pixmap.scaled(300, 300, aspectRatioMode=True))
    pixmap.setGeometry(200, 80, 300, 300)
    pixmap.show()
        


def select_image(label):
    options = QFileDialog.Options()
    file_path, _ = QFileDialog.getOpenFileName(None, "Resim Seç", "", "Resim Dosyalari (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
    if file_path:
        pixmap = QPixmap(file_path)
        label.setPixmap(pixmap.scaled(label.size(), aspectRatioMode=True))

def select_option(combo_box, label):
    selected_option_text = combo_box.currentText()
    selected_option_index = combo_box.currentIndex()
    label.setText(f"Seçilen: {selected_option_text} (Index: {selected_option_index})")
    
    if selected_option_index == 1:
        # 1. seçenek seçildiğinde yapılacak işlemi buraya yazabilirsiniz
        binaryimage=binaryimage(file_path)
        pixmap=QPixmap.fromImage(binaryimage)
        
        
        



if __name__ == '__main__':
    main()
