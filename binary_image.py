from gray_scale import bgr_to_gray
import numpy as np
import cv2

def binaryimage(filepath):
    img=cv2.imread(filepath)
    #resmin boyutlarını alıyoruz
    height,width=img.shape[:2]
    # boş resim oluştuıruyoruz
    binaryimage=np.zeros((height,width),dtype=np.uint8)
    for y in range(height):
        for x in range(width):
            pixel=img[y,x]
            #herhangi bir pikselin değerini kontrol etmek için
            if (pixel < 128).any():
                binaryimage[y,x]=0
            else:
                binaryimage[y,x]=255
    return binaryimage
 
    
    
    
    
    


















