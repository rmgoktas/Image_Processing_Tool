from PIL import Image
import numpy as np



def multiplication(img1,img2):
    img1height,img1width,img1ch=img1.shape
    img2height,img2width,img2ch=img2.shape
    
    if((img1height==img2height)&(img1width==img2width)&(img1ch==img2ch)):
        
        if(img1ch==1):
            newimg=np.zeros((img1height,img1width),dtype=np.uint8)
            
            for y in range(img1height):
                for x in range(img1width):
                    img1_pixel_value=img1[y,x]
                    img2_pixel_value=img2[y,x]
                    new_value=img1_pixel_value*img2_pixel_value
                    if(new_value>255):
                        newimg[y,x]=255
                    else:
                        newimg[y,x]=new_value
            return newimg
        else:
            newimg=np.zeros((img1height,img1width,3),dtype=np.uint8)
            
            for y in range(img1height):
                for x in range(img1width):
                    img1_blue=img1[y,x,0]
                    img2_blue=img2[y,x,0]
                    blue_value=img1_blue*img2_blue
                    if(blue_value>255):
                        newimg[y,x,0]=255
                    else:
                        newimg[y,x,0]=blue_value
                    img1_green=img1[y,x,1]
                    img2_green=img2[y,x,1]
                    green_Value=img1_green*img2_green
                    if(green_Value>255):
                        newimg[y,x,1]=255
                    else:
                        newimg[y,x,1]=green_Value
                    img1_red=img1[y,x,2]
                    img2_red=img2[y,x,2]
                    red_value=img1_red*img2_red
                    if(red_value>255):
                        newimg[y,x,2]=255
                    else:
                        newimg[y,x,2]=red_value
            return newimg
    else:
        print("Resimler ayni boyutta veya formatta degil")
                    
                    
    

                    
                    
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    