import numpy as np

def bgr_to_gray(img):
    height,width,_=img.shape
    
    gray_img=np.zeros((height,width),dtype=np.uint8)
    
    
    for y in range(height):
        for x in range(width):
            blue=img[y,x,0]
            green=img[y,x,1]
            red=img[y,x,2]
            
            gray_pixel=(int(blue)+int(green)+int(red))//3
            gray_img[y,x]=gray_pixel
            
    return gray_img
            
    
    
    



