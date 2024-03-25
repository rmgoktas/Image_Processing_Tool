import numpy as np

def threshold(img,maxvalue,adaptivetype,blocksize):
    
    height,width=img.shape
    
    blocks = []
    if(adaptivetype==1):
        new_img=np.zeros((height,width),dtype=np.uint8)
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                blocks.append(block) 
        
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                mean_value=mean(block)
                
                for k in range(block.shape[0]):
                    for l in range(block.shape[1]):
                        if(block[k,l]<mean_value/2):
                            block[k,l]=0
                        else:
                            block[k,l]=maxvalue
                new_img[y:y+blocksize, x:x+blocksize] = block
        return new_img      
    if(adaptivetype==2):
        new_img=np.zeros((height,width),dtype=np.uint8)
        for y in range(0,height,blocksize):
            for x in range(0,width,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                blocks.append(block) 
        
        for y in range(0,height,blocksize):
            for x in range(0,height,blocksize):
                block = img[y:y+blocksize, x:x+blocksize]
                mean_value=mean(block)
                
                for k in range(block.shape[0]):
                    for l in range(block.shape[1]):
                        if(block[k,l]<mean_value/2):
                            block[k,l]=maxvalue
                        else:
                            block[k,l]=0
                new_img[y:y+blocksize, x:x+blocksize] = block
        return new_img
           
def mean(block):
    height, width = block.shape
    total_value = 0
    
    for y in range(height):
        for x in range(width):
            total_value += block[y, x]
    
    mean_value = total_value / (height * width)
    
    return mean_value
    
    








