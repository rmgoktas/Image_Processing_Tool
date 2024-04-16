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
    window.setGeometry(150, 150, 400, 400)  # (x, y, width, height)
    
    # Resim etiketi
    image_label = QLabel(window)
    image_label.setGeometry(50, 80, 300, 300)
    


    # Seçenekler listesi
    options_list = ["Binary Dönüşüm", "Zoom", "Topla","Çarp","Adaptif Eşikleme","Blurlama"]
    combo_box = QComboBox(window)
    combo_box.setGeometry(50, 50, 200, 30)
    combo_box.addItems(options_list)
    # Pencereyi göster
    window.show()
    
    # Uygulamayı çalıştır
    sys.exit(app.exec_())
    
    
def select_option(combo_box, label):
    selected_option_text = combo_box.currentText()
    selected_option_index = combo_box.currentIndex()
    label.setText(f"Seçilen: {selected_option_text} (Index: {selected_option_index})")
    
    if selected_option_index == 1:
        # 1. seçenek seçildiğinde yapılacak işlemi buraya yazabilirsiniz
        pass
        

if __name__ == '__main__':
    main()   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    