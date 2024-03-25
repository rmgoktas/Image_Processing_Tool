from PIL import Image

def addition(path1,path2):
    
    img1=Image.open(path1)
    img2=Image.open(path2)
    
    p1w,p1h=img1.size
    p2w,p2h=img2.size
    
    if p1w==p2w and p1h==p2h:
        #renk modu,boyut,arkaplan rengi
        yeni_resim=Image.new("BGR",(p1w,p1h),"white")
        
        for x in range(p1w):
            for y in range(p1h):
                p1=img1.getpixel((x,y))
                p2=img2.getpixel((x,y))
                
                yeni_pixel=tuple([sum(renkler)for renkler in zip (p1,p2)])
                yeni_resim.putpixel((x,y),yeni_pixel)
        
        yeni_resim.show()
    else:
        print("Resimler Ayni Boyutta Degil")
        return