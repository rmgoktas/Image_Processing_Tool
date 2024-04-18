import cv2
import numpy as np

def rescale_with_black(image, scale_percent):
    # Orjinal resmin boyutları
    height, width = image.shape[:2]
    
    # Yeni boyutları hesapla
    new_width = int(width * scale_percent / 100)
    new_height = int(height * scale_percent / 100)
    
    # Yeniden boyutlandırma işlemi
    resized_image = cv2.resize(image, (new_width, new_height))
    
    # Siyah bir arka plan oluştur
    black_background = np.zeros((height, width, 3), np.uint8)
    
    # Yeniden boyutlandırılmış resmi siyah arka planın merkezine yerleştir
    x_offset = (width - new_width) // 2
    y_offset = (height - new_height) // 2
    black_background[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_image
    
    return black_background

# Resmi yükle
image = cv2.imread('peppers.jpeg')

# Yeniden boyutlandır ve siyah kısmı ekleyerek resmi döndür
resized_image = rescale_with_black(image, 50) # Ölçek yüzde olarak verilir

# Sonucu göster
cv2.imshow('Resized with Black Background', resized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
