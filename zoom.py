from PIL import Image
import numpy as np

def resize_image(img, scale):
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
            resized_img[y, x] = img[resized_y, resized_x]
    
    return resized_img
