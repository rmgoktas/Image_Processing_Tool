import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QComboBox

file_path = None

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
    options_list = ["İşlem Seç","Gri Dönüşüm", "Binary Dönüşüm", "Görüntü döndürme", "Görüntü Kirpma", "Görüntü yak-uzak", "Renk uzayi",
                    "Germe-Genişletme","Resim Toplama","Resim Çarpma","Parlaklik Arttirma","Konvolüsyon(Gauss)","Adaptif Eşikleme",
                    "Sobel kenar bulma","Salt-Pepper","Blurring","Morfolojik işlemler"]
    combo_box = QComboBox(window)
    combo_box.setGeometry(50, 50, 200, 30)
    combo_box.addItems(options_list)
    
    # Combo box değişim sinyalini bir işlevle bağlayın
    combo_box.currentIndexChanged.connect(lambda: select_option(combo_box))
    
    # Pencereyi göster
    window.show()
    
    # Uygulamayı çalıştır
    sys.exit(app.exec_())

def select_option(combo_box):
    selected_option_index = combo_box.currentIndex()
    
    if selected_option_index == 1:
        subprocess.run(["python", "gray_scale.py"])
    elif selected_option_index == 2:
        subprocess.run(["python", "binary_image.py"])
    elif selected_option_index == 3:
        subprocess.run(["python", "resimDondurme.py"])
    elif selected_option_index == 4:
        subprocess.run(["python", "image_cropping.py"])
    elif selected_option_index == 5:
        subprocess.run(["python", "zoom.py"])
    elif selected_option_index == 6:
        subprocess.run(["python", "renkUzayi.py"])
    elif selected_option_index == 7:
        subprocess.run(["python", "stretching_expansion.py"])    
    elif selected_option_index == 8:
        subprocess.run(["python", "addition.py"])
    elif selected_option_index == 9:
        subprocess.run(["python", "multiplication.py"])    
    elif selected_option_index == 10:
        subprocess.run(["python", "parlaklikArtirmaAzaltma.py"])
    elif selected_option_index == 11:
        subprocess.run(["python", "gauss.py"]) 
    elif selected_option_index == 12:
        subprocess.run(["python", "threshold.py"])
    elif selected_option_index == 13:
        subprocess.run(["python", "kenarBulma.py"])
    elif selected_option_index == 14:
        subprocess.run(["python", "salt_pepper.py"])
    elif selected_option_index == 15:
        subprocess.run(["python", "boxblur.py"])
    elif selected_option_index == 16:
        subprocess.run(["python", "morfolojikIslemler.py"])
if __name__ == '__main__':
    main()
